# purpose
Mount a previous context bundle to recover state after a context explosion.

# args
bundle_path: agents/context-bundles/{bundle}

# workflow
- read ${bundle_path}
- dedupe reads and reconstruct key findings
- print a concise recap (≤200 tokens) and list file paths to re‑open
- advise next action prime (e.g., prime_bug or prime_feature)
