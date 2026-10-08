# ADR-0009: Static dashboard on GitHub Pages, with a live-reload local server

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The founder wants to see analytics for every run on a web page, preferably from git, and wants the page to update by itself during local work.

## Decision
- **Static site, no framework:** plain HTML/CSS/JS in `apps/dashboard/static/`, data gathered by `build.py` into one `data.json` from files already in git (`data/metrics/index.json`, latest outputs). Nothing to install.
- **Charts** follow the dataviz method: one series per chart (no dual axes), a validated ordinal blue ramp for grades A–D (light and dark), status colors always paired with a word, hover/focus tooltips, a table view, and dark mode with its own validated steps.
- **Untrusted text:** data from runs is inserted with `textContent`; the PRD viewer renders Markdown through DOMPurify (falls back to plain text if the CDN is unreachable).
- **Local live reload:** `serve.py` (standard library) watches the data and dashboard folders, rebuilds on change, and exposes `/__version`; the page polls it and redraws without a full reload.
- **GitHub Pages** deploy on pushes to `main` and after each `prd-agent` run (those commits don't trigger workflows themselves).

## Consequences
- Anyone with the Pages link can see the dashboard; it is public on most plans.
- The PRD viewer needs the jsDelivr CDN for formatted Markdown; offline it shows plain text.
