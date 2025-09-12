# Convenience wrappers for R&D context-engineering workflow.
# Note: Slash-commands are executed inside your Claude/agent environment.
# These make targets focus on repo hygiene and bundle utilities.

PY=python3

# Lint the universal memory file
lint-memory:
	$(PY) scripts/lint_memory.py

# Create a new context bundle and append a PRIME event
# Usage: make bundle-new PURPOSE="Quick codebase understanding"
bundle-new:
	$(PY) scripts/context_bundle_writer.py --kind prime --payload "{\"purpose\":\"$(PURPOSE)\"}"

# Append a READ event to an existing bundle
# Usage: make bundle-read BUNDLE="agents/context-bundles/20250101T000000Z_abcd1234" PATH="src/main.py"
bundle-read:
	$(PY) scripts/context_bundle_writer.py --bundle "$(BUNDLE)" --kind read --payload "{\"path\":\"$(PATH)\"}"

# Append key findings
# Usage: make bundle-findings BUNDLE="..." BULLETS='["X fixed","Y pending"]'
bundle-findings:
	$(PY) scripts/context_bundle_writer.py --bundle "$(BUNDLE)" --kind key_findings --payload "{\"bullets\":$(BULLETS)}"

# Summarize a bundle and optionally write a report
# Usage: make bundle-load BUNDLE="agents/context-bundles/.../bundle.jsonl" REPORT=1
bundle-load:
	$(PY) scripts/load_bundle.py "$(BUNDLE)" $(if $(REPORT),--write-report,)

.PHONY: lint-memory bundle-new bundle-read bundle-findings bundle-load
