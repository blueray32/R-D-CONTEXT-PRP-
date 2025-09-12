# purpose
Launch a detached primary agent to run a plan while freeing the main loop.

# args
model: opus
report_file: reports/quick_plan/{task}_{ts}.report.md
workdir: .

# workflow
- ensure directory for ${report_file}
- generate a quick plan for {task} using minimal reads
- append progress logs to ${report_file}
- on completion, rename ${report_file} → ${report_file.replace('.report.md','_completed.md')}
- output a one‑screen recap (≤200 tokens)
