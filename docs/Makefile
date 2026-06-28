# Minimal Sphinx/MkDocs helper Makefile.
#
# Project layout assumes mkdocs.yml at repo root.

.PHONY: help html serve clean

help:
	@echo "Targets:"
	@echo "  html   - build static site"
	@echo "  serve  - live-reload dev server"
	@echo "  clean  - remove site/ build artefacts"

html:
	mkdocs build

serve:
	mkdocs serve

clean:
	rm -rf site/