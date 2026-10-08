# ADR-0003: Guardrails run first: rules, then a Claude review

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
Transcripts can contain personal data, prompt-injection text, off-topic content, or risky product ideas. Every later agent reads the transcript, so problems must be caught once, at the start.

## Decision
1. **Rule-based checks first** (free, fast, predictable): size limit, mask personal data and secrets (email, phone, SSN, card numbers with a Luhn check, IP addresses, API keys), spot common injection phrases.
2. **Claude review second**, on the already-masked text, with a fixed JSON schema: on topic? injection? EU AI Act risk level? harm concerns?
3. **Three outcomes:** `allow`; `warn` (continue, and pass notes to the PRD Writer, which must address them); `block` (stop; no PRD). Block only for off-topic text, unacceptable EU AI Act risk, clear harm, or a transcript that is too long. An injection attempt is a warning, not a block, because later agents already treat the transcript as data.
4. Saved reports store **counts** of masked data, never the values.

## Consequences
- Personal data never reaches the PRD Writer or the saved outputs.
- Rules can miss things and can over-match; the Claude review is the safety net. Both are covered by tests and fixtures in `evals/fixtures/`.
- One extra API call per run (low effort, small output).
