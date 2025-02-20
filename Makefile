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

.PHONY: help
## Show commands from this file
help : Makefile
	@sed -n 's/^##//p' $<
