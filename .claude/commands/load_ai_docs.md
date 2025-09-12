# purpose
Delegate web/doc ingestion to sub‑agents; keep tokens out of the primary context.

# variables
seed_file: ./AI_DOCS_README.md
out_dir: agents/ai-docs
max_agents: 8

# workflow
- read ${seed_file}
- for each URL in the list (up to ${max_agents} concurrent):
  - spawn sub‑agent with system prompt for fetch/scrape
  - save raw fetch to ${out_dir}/{hash}.raw.txt
  - write a 150‑token summary to ${out_dir}/{hash}.summary.md
- return only a table of URL → summary path

# report
- file: reports/load_ai_docs_{ts}.md
- include: counts, failures, retry hints
