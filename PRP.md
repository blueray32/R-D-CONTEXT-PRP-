# PRP — Mastering Context Engineering for Agent Performance (R&D Best Practices)

**Owner:** Ciaran Cox  
**Date:** 2025‑09‑10  
**Goal:** Implement a repeatable Reduce & Delegate (R&D) context‑engineering workflow that produces faster, more reliable, and cheaper agent runs by shrinking the primary context window and offloading heavy work to focused agents.

## 1) Summary (Why / What)
A focused agent is a performant agent. This PRP operationalizes R&D best practices:
- **Reduce** what enters the primary agent’s context at boot and during loops.
- **Delegate** token‑heavy tasks to sub‑agents or background primary agents and persist outcomes as files/bundles.

**Desired outcome:** Boot with a slim, universal memory; load only task‑specific tools/context on demand; orchestrate sub‑agents/background agents for heavy I/O; maintain replayable **context bundles** so work continues cleanly after context explosions.

## 2) Success Criteria (Definition of Done)
1. **Boot budget:** Primary agent starts with ≥90% free context; always‑on memory ≤500 tokens.
2. **MCP hygiene:** No default MCP servers autoloaded; task runs pass in an explicit MCP config.
3. **Priming over memory:** Task types use **prime commands** (bug/feature/docs/CC) to read only the minimal files needed.
4. **Delegation:** Web/doc reads and other token‑heavy steps run in **sub‑agents** or **background primary agents** and write artifacts to disk.
5. **Context bundles:** Each significant run writes an append‑only bundle (prompt + reads + key findings). A new agent can **/load** a bundle to remount state to ~70% without re‑reading everything.
6. **Reporting:** Background agents write to a report file and rename it on completion.

## 3) Scope / Non‑Goals
- **In scope:** Agent context hygiene, MCP configuration discipline, priming commands, sub‑agent workflows, background agent delegation, context bundle logging, Makefile/CLI wrappers, CI lint.
- **Out of scope:** New product features beyond these workflow changes; model/provider swaps; IDE migration.

## 4) Inputs & Artifacts
**Inputs**
- Existing repo and Claude‑style slash‑command support.
- Optional MCP servers (e.g., web fetch / Firecrawl) available but **not** autoloaded.

**Artifacts produced**
- `memory/concise.md` — tiny universal memory file.
- `.claude/commands/prime_*.md` — reusable primes (bug, feature, docs, cc).
- `.claude/commands/background.md` — fires a background instance + report file.
- `.claude/commands/load_ai_docs.md` — sub‑agent doc ingestion.
- `.claude/commands/load_bundle.md` — remount prior state.
- `agents/context-bundles/…` — append‑only run trails.
- `reports/**` — status & outputs from background/prime runs.
- `configs/mcp/firecrawl.json` — example strict per‑task MCP config.
- `scripts/lint_memory.py` — CI lint for memory size.
- `scripts/context_bundle_writer.py`, `scripts/load_bundle.py` — bundle utilities.
- `Makefile` — convenience wrappers.
- `.github/workflows/lint-memory.yml` — CI enforcement.

## 5) Constraints & Risks
- **Risk (coordination):** Sub‑agent chatter or oversized outputs can re‑bloat context.  
  **Mitigation:** Return **summaries + file paths**, not raw dumps.
- **Risk (memory creep):** Teams expand universal memory over time.  
  **Mitigation:** Hard cap lines/tokens; everything else moves to primes.
- **Risk (tool sprawl):** Loading many MCP servers “just in case.”  
  **Mitigation:** Enforce explicit per‑task MCP configs.

## 6) Implementation Plan (R&D in action)

### Phase A — Reduce
1. **Kill default MCP autoload**
   - Remove `default.mcp.json` (or equivalent).
   - Create per‑task configs (e.g., `configs/mcp/firecrawl.json`).
   - Run tasks with a strict flag in your tool (e.g., `--strict-mcp-config <path>`).

2. **Slim universal memory**
   - Replace the giant always‑on memory file with `memory/concise.md` (≤50 lines).
   - Keep only **universal, always‑true** rules (style, output format, safety, short glossary).
   - Add a CI check that fails if the file exceeds token/line caps.

3. **Adopt context priming**
   - Add primes:
     - `.claude/commands/prime_bug.md`
     - `.claude/commands/prime_feature.md`
     - `.claude/commands/prime_docs.md`
     - `.claude/commands/prime_cc.md`
   - **Prime template (all primes follow this):**
     - **Purpose** — one‑line intent.
     - **Run** — minimal steps for this task type.
     - **Read** — explicit file list/globs (keep tiny).
     - **Report** — where to write status/summary.

**Gate A:** Boot context free ≥90%; memory ≤500 tokens; no MCP servers loaded by default.

### Phase B — Delegate (Sub‑agents)
4. **Sub‑agent doc/web ingestion**
   - Use `.claude/commands/load_ai_docs.md` with a **system‑prompted** workflow:
     **Purpose → Variables → Workflow → Report format**.
   - Steps: primary agent reads a seed file → spawns N sub‑agents to fetch/scrape docs (one URL per sub‑agent) → each writes outputs to `agents/ai-docs/…` and a concise summary.
   - Ensure tokens burn inside sub‑agents; primary receives only summaries + paths.

**Gate B:** Primary context remains under ~10k tokens during ingestion; outputs saved; summaries generated.

### Phase C — Advanced R&D (Bundles + Background)
5. **Context bundles (append‑only logs)**
   - Use hooks or the provided scripts so each **read/search/prompt** appends to `agents/context-bundles/<timestamp>_<session>/bundle.jsonl`:
     - `prompt` (purpose + arguments)
     - `reads` (deduped file list)
     - `key_findings` (concise bullets)
   - Use the provided loader script to dedupe reads, reconstruct key findings, and print a **one‑screen recap**.

6. **Background primary agent delegation**
   - `.claude/commands/background.md` starts a detached agent using arguments (model, task, report file path, working dir).
   - The background agent writes progress to `reports/<task>/<timestamp>.report.md` and **renames** it to `…_completed.md` when done.

**Gate C:** Able to remount a blown context to ~70% state from a bundle; background agent produces a completed report file.

## 7) Validation & QA Gates
- **Gate A (Reduce):** Boot audit shows ≥90% free, ≤500‑token memory, 0 MCP servers loaded.
- **Gate B (Delegate):** Sub‑agent run saves N outputs; primary agent token use stays under the cap; report includes URL → file mapping.
- **Gate C (Bundles/Background):** Bundle loader reconstructs prior state with deduped reads; background report file is present and renamed to `…_completed.md`.
- **Smoke tests:** Run a sample “docs refresh” and “quick plan” to verify end‑to‑end R&D flow.

## 8) Metrics to Track
- Startup tokens (before/after).  
- Total tokens burned **in primary** vs **in sub/background agents**.  
- Latency per task stage (prime → ingest → plan → implement).  
- One‑shot success rate of out‑loop tasks.  
- Number of re‑primes required.

## 9) Rollout & Ops
- Land the memory and command changes on a feature branch; run against one repo for 48 hours; compare metrics.  
- If gains ≥20% primary‑token reduction and stable success rate, roll to all projects.  
- Add a weekly lint to block memory file growth; review MCP configs in PRs.

## 10) Team Playbook
- Keep the universal memory tiny; everything else is a **prime**.  
- Never autoload MCP servers; pass explicit configs per run.  
- Use sub‑agents for web/doc I/O and heavy reads.  
- Always write a bundle; reload bundles when the window explodes.  
- Prefer background delegation to get out of the loop.
