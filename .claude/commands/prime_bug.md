# purpose
Rapidly prime the agent to diagnose and fix a specific bug with minimal context usage.

# run
- read ./README.md
- read ./CONTRIBUTING.md
- read ./src/**/{bug_area}/*
- identify root cause hypotheses (≤5 bullets)
- propose fix steps with file paths and function names
- write summary to reports/prime/prime_bug_{bug_area}.md (≤250 tokens)

# read
- README.md
- CONTRIBUTING.md
- src/**/{bug_area}/*

# report
- file: reports/prime/prime_bug_{bug_area}.md
- include: key files, suspected cause, next actions
