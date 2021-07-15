.PHONY: qa/all
qa/all:  ## Run pre-commit QA pipeline on all files
	pre-commit run --all-files

.PHONY: qa/coverage
qa/coverage:  ## Coverage report
	poetry run coverage run -m --source=src pytest tests
	poetry run coverage report

.DEFAULT_GOAL := help
.PHONY: help
help:
	@grep --no-filename -E '^[a-zA-Z_\/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
