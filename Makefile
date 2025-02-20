# Environment =================================================================
.PHONY: environment
## create virtual environment for dbt project
environment:
	@brew upgrade pyenv
	@pyenv install -s 3.11.9
	@pyenv virtualenv 3.11.9 user-api
	@pyenv local user-api
	@PYTHONPATH=. python -m pip install --upgrade pip
	@make requirements
	@

.PHONY: delete-environment
## create virtual environment for dbt project
delete-environment:
	@pyenv virtualenv-delete user-api
	@rm .python-version

.PHONY: requirements
## install development requirements
requirements:
	@PYTHONPATH=. python -m pip install -U -r requirements.txt

.PHONY: requirements-lint
## install lint requirements
requirements-lint:
	@PYTHONPATH=. python -m pip install -r requirements.lint.txt

# Style & Lint ================================================================

.PHONY: check-style
## run code style checks with black
check-style:
	@echo ""
	@echo "Check Style"
	@echo "==========="
	@echo ""
	@make apply-style
	@make check-black
	@make check-flake8
	@echo "Checks finished"

.PHONY: check-black
## run code style checks with black
check-black:
	@echo "Running Black checks"
	@echo "===================="
	@echo ""
	@python -m black --check . && echo "\n\nSuccess\n" || (echo "\n\nFailure\n\nRun \"make apply-style\" to apply style formatting to your code\n" && exit 1)

.PHONY: check-flake8
## run code style checks with black
check-flake8:
	@echo "Running Flake8 checks"
	@echo "====================="
	@echo ""
	@find ./ -type f -name '.flake8_report.txt' -exec rm -rf {} +;
	@python -m flake8 --output-file=.flake8_report.txt --config=flake8.ini . ; cat .flake8_report.txt

.PHONY: apply-style
## run black to fix code style
apply-style:
	@python -m black -t py39 .


.PHONY: help
## Show commands from this file
help : Makefile
	@sed -n 's/^##//p' $<
