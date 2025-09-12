# purpose
Prime for editing Claude/agent command files and configs with strict context budget.

# run
- read ./.claude/README.md
- read ./.claude/commands/**
- read ./configs/mcp/*.json
- enumerate command coverage, overlaps, and dead code (≤6 bullets)
- propose renames or merges
- write summary to reports/prime/prime_cc.md (≤250 tokens)

# read
- .claude/README.md
- .claude/commands/**
- configs/mcp/*.json

# report
- file: reports/prime/prime_cc.md
- include: risky commands, missing primes, quick wins
