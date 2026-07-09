.PHONY: build tables readme validate all

build:
	python3 scripts/build_database.py

tables:
	python3 scripts/generate_tables.py

readme: tables
	python3 scripts/update_readme.py

validate:
	python3 scripts/validate_links.py --fail-on-broken

all: build tables readme
	@echo "Database + README regenerated. Run 'make validate' to check links."
