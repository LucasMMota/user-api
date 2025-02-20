# Environment =================================================================
.PHONY: environment
## create virtual environment for dbt project
environment:
	@brew upgrade pyenv
	@pyenv install -s 3.11.9
	@pyenv virtualenv 3.11.9 picpay-api
	@pyenv local picpay-api
	@PYTHONPATH=. python -m pip install --upgrade pip
	@make requirements
	@

.PHONY: delete-environment
## create virtual environment for dbt project
delete-environment:
	@pyenv virtualenv-delete picpay-api
	@rm .python-version

.PHONY: requirements
## install development requirements
requirements:
	@PYTHONPATH=. python -m pip install -U -r requirements.txt
