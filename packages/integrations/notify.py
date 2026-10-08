"""Gmail alerts: email a short summary when a PRD is created or updated, or when a run has problems.

Events (choose with ALERT_ON, comma-separated; default: all):
  new          a PRD was written for a transcript that had none
  updated      the PRD changed (the email lists which sections)
  blocked      guardrails stopped the run
  quality_fail the quality gate failed
  error        a pipeline step failed
  budget       the cost budget was reached and optional steps were skipped

Sending uses Gmail's SMTP server with an app password (Python standard library only):
  GMAIL_ADDRESS       the Gmail account that sends the alert
  GMAIL_APP_PASSWORD  an app password for that account (not your normal password)
  ALERT_TO            who receives it (comma-separated); defaults to GMAIL_ADDRESS
  DASHBOARD_URL       optional link to the dashboard

If these are not set, nothing is sent and the email is saved as data/outputs/<name>/alert.eml.
"""

from __future__ import annotations

import html
import os
import re
import smtplib
import ssl
from dataclasses import dataclass, field
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST, SMTP_PORT = "smtp.gmail.com", 465
EVENTS = ("new", "updated", "blocked", "quality_fail", "error", "budget")
SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Alert:
    events: list[str]
    subject: str
    text: str
    html: str
    changes: dict = field(default_factory=dict)


def split_sections(prd: str) -> dict[str, str]:
    """Section title -> body text, e.g. '10. Security and Privacy' -> '...'."""
    parts = SECTION_RE.split(prd)
    # parts = [preamble, num, title, body, num, title, body, ...]
    return {f"{parts[i]}. {parts[i + 1]}": parts[i + 2].strip() for i in range(1, len(parts) - 2, 3)}


def section_changes(old: str | None, new: str | None) -> dict[str, list[str]]:
    if not new:
        return {"added": [], "changed": [], "removed": []}
    old_s, new_s = split_sections(old or ""), split_sections(new)
    return {
        "added": [t for t in new_s if t not in old_s],
        "changed": [t for t in new_s if t in old_s and " ".join(old_s[t].split()) != " ".join(new_s[t].split())],
        "removed": [t for t in old_s if t not in new_s],
    }


def detect_events(metrics: dict, old_prd: str | None, new_prd: str | None) -> tuple[list[str], dict]:
    events, changes = [], section_changes(old_prd, new_prd)
    if metrics["status"] == "blocked":
        events.append("blocked")
    elif new_prd and not old_prd:
        events.append("new")
    elif new_prd and any(changes.values()):
        events.append("updated")
    if metrics.get("quality_gate") == "fail":
        events.append("quality_fail")
    if any("error" in s for s in metrics["steps"]):
        events.append("error")
    if (metrics.get("budget") or {}).get("skipped"):
        events.append("budget")
    return events, changes


def _links(name: str, issues: list[int]) -> dict[str, str]:
    repo = os.environ.get("GITHUB_REPOSITORY")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    links = {}
    if repo:
        links["PRD"] = f"{server}/{repo}/blob/main/data/outputs/{name}/PRD.md"
        links["Run log"] = f"{server}/{repo}/blob/main/data/decisions/RUN_LOG.md"
        links.update({f"Issue #{n}": f"{server}/{repo}/issues/{n}" for n in issues})
    if os.environ.get("DASHBOARD_URL"):
        links["Dashboard"] = os.environ["DASHBOARD_URL"]
    return links


def build_alert(metrics: dict, events: list[str], changes: dict, issues: list[int] | None = None) -> Alert:
    name = Path(metrics["transcript"]).stem
    ev = metrics.get("evaluation") or {}
    rv = metrics.get("review") or {}
    verdict = (ev.get("verdict") or "").upper().replace("_", "-") or "not scored"
    headline = {"new": "New PRD", "updated": "PRD updated", "blocked": "Run blocked"}.get(
        next((e for e in events if e in ("new", "updated", "blocked")), ""), "PRD run")
    flags = [x for x, on in (("quality gate FAILED", "quality_fail" in events),
                             ("step failed", "error" in events), ("budget reached", "budget" in events)) if on]
    subject = f"[PRD-Agent] {headline}: {name}"
    if metrics["status"] != "blocked":
        subject += f" | verdict {verdict} | quality {metrics.get('quality_gate', '-')}"
    if flags:
        subject += " | " + ", ".join(flags)

    rows = [("Transcript", name), ("Run", metrics["run_id"]), ("Status", metrics["status"]),
            ("Guardrails", metrics["guardrails"]["decision"])]
    if metrics["status"] == "blocked":
        rows.append(("Why blocked", "; ".join(metrics["guardrails"]["reasons"])))
    else:
        rows += [("Verdict", f"{verdict} (average {ev.get('average', '-')}/5)" if ev.get("verdict") else verdict),
                 ("Quality gate", str(metrics.get("quality_gate", "-"))),
                 ("Reviewer rubric", f"{rv.get('rubric_average', '-')}/5"),
                 ("Revised", "yes" if metrics.get("revised") else "no")]
    rows += [("Cost", f"${metrics['total_cost_usd']:.2f}"), ("Time", f"{metrics['total_duration_s']:.0f}s")]
    failed = [s["agent"] for s in metrics["steps"] if "error" in s]
    if failed:
        rows.append(("Failed steps", ", ".join(failed)))
    budget = metrics.get("budget") or {}
    if budget.get("skipped"):
        rows.append(("Budget", f"${budget['limit_usd']:.2f} reached; skipped {', '.join(budget['skipped'])}"))

    change_lines = [f"{label}: {', '.join(items)}" for label, items in
                    (("Added", changes.get("added", [])), ("Changed", changes.get("changed", [])),
                     ("Removed", changes.get("removed", []))) if items]
    scores = ev.get("scores") or {}
    links = _links(name, issues or [])

    text = "\n".join([subject, ""] + [f"{k}: {v}" for k, v in rows]
                     + ([""] + ["Sections:"] + change_lines if change_lines else [])
                     + ([""] + ["Scores:"] + [f"  {k}: {v}/5" for k, v in scores.items()] if scores else [])
                     + ([""] + [f"{k}: {v}" for k, v in links.items()] if links else []))

    e = html.escape  # everything shown comes from model output or files: escape it
    body = [f"<h2>{e(headline)}: {e(name)}</h2>", "<table cellpadding='4'>"]
    body += [f"<tr><td><b>{e(k)}</b></td><td>{e(str(v))}</td></tr>" for k, v in rows]
    body.append("</table>")
    if change_lines:
        body.append("<h3>Sections</h3><ul>" + "".join(f"<li>{e(c)}</li>" for c in change_lines) + "</ul>")
    if scores:
        body.append("<h3>Scores</h3><ul>" + "".join(f"<li>{e(k)}: {e(str(v))}/5</li>" for k, v in scores.items()) + "</ul>")
    if links:
        body.append("<p>" + " · ".join(f"<a href='{e(u, quote=True)}'>{e(k)}</a>" for k, u in links.items()) + "</p>")
    return Alert(events, subject, text, "\n".join(body), changes)


def to_email(alert: Alert, sender: str, recipients: list[str]) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = alert.subject, sender, ", ".join(recipients)
    msg.set_content(alert.text)
    msg.add_alternative(alert.html, subtype="html")
    return msg


def wanted_events(env: dict) -> set[str]:
    raw = env.get("ALERT_ON", "").strip()
    return set(EVENTS) if not raw else {e.strip() for e in raw.split(",") if e.strip() in EVENTS}


def send_gmail(msg: EmailMessage, sender: str, app_password: str, smtp_factory=smtplib.SMTP_SSL) -> None:
    with smtp_factory(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context(), timeout=30) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)


def notify(metrics: dict, out_dir: Path, old_prd: str | None, issues: list[int] | None = None,
           env: dict | None = None, smtp_factory=smtplib.SMTP_SSL) -> dict:
    """Decide whether to alert, then send by Gmail or save alert.eml. Returns what happened."""
    env = dict(os.environ) if env is None else env
    prd_path = out_dir / "PRD.md"
    new_prd = prd_path.read_text() if metrics["status"] == "completed" and prd_path.exists() else None
    events, changes = detect_events(metrics, old_prd, new_prd)
    events = [e for e in events if e in wanted_events(env)]
    if not events:
        return {"sent": False, "events": [], "reason": "nothing to report"}

    alert = build_alert(metrics, events, changes, issues)
    sender, password = env.get("GMAIL_ADDRESS"), env.get("GMAIL_APP_PASSWORD")
    recipients = [r.strip() for r in (env.get("ALERT_TO") or sender or "").split(",") if r.strip()]
    msg = to_email(alert, sender or "prd-agent@localhost", recipients or ["you@localhost"])
    info = {"events": events, "subject": alert.subject, "changes": changes}

    if not (sender and password):
        (out_dir / "alert.eml").write_bytes(bytes(msg))
        return {**info, "sent": False, "reason": "GMAIL_ADDRESS or GMAIL_APP_PASSWORD not set; saved alert.eml"}
    try:
        send_gmail(msg, sender, password, smtp_factory)
    except (smtplib.SMTPException, OSError) as e:
        (out_dir / "alert.eml").write_bytes(bytes(msg))
        return {**info, "sent": False, "reason": f"send failed: {type(e).__name__}; saved alert.eml"}
    return {**info, "sent": True, "recipients": len(recipients)}
