# universal essentials (≤50 lines)
- Output style: terse, structured, file‑first.
- Always prefer primes over ad‑hoc broad reads.
- Summarize to ≤250 tokens unless asked for full detail.
- Never autoload MCP; require explicit per‑task config.
- When heavy I/O is needed, delegate to sub/background agents and persist artifacts.
- After long runs, append a context bundle; reload bundles when the window explodes.
