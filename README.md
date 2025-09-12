# Context Engineering PRP Pack (R&D)

This pack contains:
- A complete PRP (`PRP.md`)
- Slash-commands in `.claude/commands/`
- A tiny universal memory (`memory/concise.md`)
- Example MCP config (`configs/mcp/firecrawl.json`)
- Context bundle utilities (`scripts/*.py`)
- A Makefile with wrappers (`Makefile`)
- CI lint for memory size (`.github/workflows/lint-memory.yml`)

## Quickstart
- Keep `memory/concise.md` ≤ 50 lines and ≤ ~500 tokens (enforced by CI).
- Use the slash-commands inside Claude/agent environment as reusable primes.
- Manage bundles locally:
  - `make bundle-new PURPOSE="Quick understanding"`
  - `make bundle-read BUNDLE="<dir>" PATH="src/main.py"`
  - `make bundle-findings BUNDLE="<dir>" BULLETS='["Risk A","Risk B"]'`
  - `make bundle-load BUNDLE="agents/context-bundles/<...>/bundle.jsonl" REPORT=1`

> Note: Sub-agent and background execution itself happens inside your agent runtime; these files provide structure, prompts, and repo hygiene.
