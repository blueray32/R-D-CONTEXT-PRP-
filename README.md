
R&D Context Engineering PRP (Reduce & Delegate)

Goal: Make agents faster, cheaper, and more reliable by Reducing what hits the primary context and Delegating token-heavy work to focused agents—while keeping a replayable paper trail.

Why this exists (the problem it solves)

Large context windows feel powerful… until they don’t. Loading “everything” leads to:
	•	Latency: slow plans, slow loops.
	•	Cost: millions of tokens burned on re-reads.
	•	Flakiness: state drifts; re-runs don’t reproduce.

R&D fixes that by treating the primary agent like a brain surgeon, not a pack mule:
	•	Reduce: boot with tiny, universal memory; load task-specific context only when needed.
	•	Delegate: hand off heavy reads (web/docs/big files) to sub-agents or a background primary; save their outputs to disk and pass back only concise summaries.

What this repo gives you (the “kit”)
	•	Tiny universal memory (memory/concise.md, CI-guarded).
	•	Task primes (.claude/commands/prime_*.md) that read only minimal files.
	•	Strict MCP discipline (configs/mcp/*.json), no autoload—everything explicit per task.
	•	Sub-agent ingestion (load_ai_docs.md) that writes files + summaries, not raw dumps.
	•	Context bundles (append-only agents/context-bundles/*.jsonl) so you can remount state after blowups.
	•	Background runs (background.md) that stream to reports/** and rename to *_completed.md.
	•	CI guardrail (.github/workflows/lint-memory.yml) to keep memory small.
	•	Makefile helpers for quick gates.

Flow at a glance

<img width="1960" height="290" alt="image" src="https://github.com/user-attachments/assets/1560c81e-2386-419c-a7e9-df1b87fcd173" />




 

Repo layout

<img width="2114" height="1022" alt="image" src="https://github.com/user-attachments/assets/58237b62-7d7c-490a-9e3a-e536e3ecfd5c" />


Quickstart (2 minutes)

<img width="966" height="378" alt="image" src="https://github.com/user-attachments/assets/31df6f80-784b-4223-a59f-2673e76dc077" />


Gates (Definition of Done)
	•	Gate A — Reduce
	•	Primary boot uses ≤500 tokens of always-on memory (≥90% free window).
	•	Zero MCP servers autoloaded; every run passes an explicit MCP config.
	•	Work starts with a prime (task-specific reads only).
	•	Gate B — Delegate
	•	Token-heavy reads happen in sub-agents or background; outputs saved to disk.
	•	Primary context stays under a safe cap during ingestion; it reads summaries + paths.
	•	Gate C — Bundles & Background
	•	Every meaningful run appends to a bundle (prompt, reads, findings).
	•	You can reload from bundle to ~70% state without rescanning everything.
	•	Background runs write reports/** and end as *_completed.md.

Metrics to track (copy into your dashboard)
	•	Startup tokens (before/after adopting tiny memory).
	•	Primary vs delegated tokens (burn split).
	•	End-to-end latency by stage (prime → ingest → plan → implement).
	•	One-shot success rate for out-of-loop tasks.
	•	Memory creep over time (CI should block).

Design principles
	•	Small, then specific: global memory stays small; everything else is a prime.
	•	Files > tokens: write artifacts to disk; pass paths + summaries between agents.
	•	Explicit tools: no “just in case” MCP servers—declare per task.
	•	Always leave breadcrumbs: bundles make your runs replayable and auditable.

FAQ

Why not just increase the model context?
Because cost, latency, and determinism suffer. R&D gives you speed and reproducibility instead.

Can I use this outside Archon/Codex?
Yes—concepts are tool-agnostic. The primes are simple markdown playbooks; scripts are plain Python.

What if bundles grow large?
They’re append-only JSONL; rotate on size/time, and keep the loader’s recap to one screen.

Contributing

Issues and PRs welcome. Keep new commands minimal, measurable, and explicit (respect Gate A/B/C).

