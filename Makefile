path := app

define Comment
	- Run `make lint-check` check all the lining related issues.
	- Run `make lint` lint the main issues.
	- Run `make auto-format` fix whatever can be fixed automatically.
	- Run `make generate-lint-reports` generate linting report in local.
	- Run `make test` run pytest in local.
	- Run `make build` build all the docker images used in the docker compose file.
	- Run `make run` run docker compose in demon mode.
	- Run `make kill` stop docker compose.
	- Run `make run-local` run application in local.
	- Run `make wiki-generate` generate wiki page and serve.
	- Run `make wiki-clean` clean static files generated for wiki serve.
	- Run `make wiki-push` push wiki page to github.
	- Run `make commit-push` push using commitizen format.
	- Run `make clean` clean all the generated files.
endef


.PHONY: lint
lint: black isort flake mypy	## Apply all the linters.


.PHONY: lint-check
lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)
	@mypy $(path)


.PHONY: black
black: ## Apply black.
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@python -m black --fast $(path)
	@echo


.PHONY: isort
isort: ## Apply isort.
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


.PHONY: flake
flake: ## Apply flake8.
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path) --exit-zero


.PHONY: mypy
mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path) || true

.PHONY: auto-format
auto-format: ## Apply auto-format.
	black .
	autopep8 --recursive --in-place --aggressive --aggressive .
	autoflake --in-place -r --ignore-init-module-imports --remove-unused-variables --remove-all-unused-imports .

.PHONY: generate-lint-reports
 generate-lint-reports: ##  generate-lint-reports
	bandit --exit-zero --format json --output bandit-report.json --recursive .
	pylint . --exit-zero > pylint-report.out
	flake8 --exit-zero --output-file=flake8.txt .
	pylint app -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --exit-zero > pylint.log

.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: test
test: ## Run the tests against the current version of Python.
	pytest


.PHONY: build
build: ## Run this to build docker images
	@docker-compose -f docker-compose.yml build


.PHONY: run
run: ## Run the app in a docker container.
	@docker-compose -f docker-compose.yml up -d

.PHONY: kill
kill: ## Stop the running docker container.
	@docker-compose -f docker-compose.yml down

.PHONY: run-local
run-local: ## Run the app locally.
	python -m uvicorn app.main:app --port 8000 --reload

.PHONY: bump
bump: ## Bump library version.
	cz bump --changelog --check-consistency
	git push --tags

.PHONY: commit-push
commit-push: ## Commit and push changes.
	git add .
	cz -n cz_commitizen_emoji c
	git push origin develop

.PHONY: wiki-generate
wiki-generate: ## Generate the wiki.
	mkdocs build
	mkdocs serve

.PHONY: wiki-clean
wiki-clean:	## Clean the wiki.
	rm -rf site/

.PHONY: wiki-push
wiki-push: ## Publish the wiki to GitHub Pages.
	mkdocs build
	mkdocs gh-deploy
	rm -rf site/

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
