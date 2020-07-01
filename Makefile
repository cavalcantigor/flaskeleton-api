# Por padrão make sem nada vai rodar 'help'
.DEFAULT_GOAL := help

# PHONY especifica que 'help' é um comando, não uma target que precisa ser
# compilada.
.PHONY: help

# Roubado de: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# grep -E faz o matchig: [COMANDO]:[espaço]<COMENTÁRIO>[espaço].
#      Nota: Em makefiles $ tem que ser trocado por $$
#
# sort: ordena os resultados alfabeticamente.
#
# awk: formata o retorno do sort em "[COMANDO]<30 espaços>[COMENTÁRIO]
#      usando ":.?##" como field separator (FS).
help:
	@echo "$$(tput bold)Comandos:$$(tput sgr0)";echo;
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s%s\n", $$1, $$2}'

clean: ## Remove arquivos temporarios
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -rf .pytest_cache/
	@rm -f coverage.xml
	@rm -rf htmlcov/
	@rm -f .coverage

test: clean  ## Executa os testes
	ENV_FOR_DYNACONF=testing pytest -rpfs

coverage: clean  ## Executa e reporta cobertura de teste no console
	ENV_FOR_DYNACONF=testing pytest --cov=app --cov-report=xml --cov-report=term-missing

coverage-html: ## Reporta cobertura de teste em html
	coverage html

check: ## Verifica qualidade da escrita de codigo
	flake8 .
	isort --check
	black --exclude "/(migrations)/" --line-length 79 --check .

container-up: ## Sobe os containers no modo detached (-d)
	docker-compose up -d

container-up-debug: ## Sobe os containers em modo de debug (sem -d)
	docker-compose up

container-clean: ## Remove volumes e imagens associadas ao container
	docker-compose rm -vsf
	docker-compose down -v --rmi all --remove-orphans

container-build: ## Rebuilda os containers
	$(MAKE) clean
	docker-compose build
	$(MAKE) up

container-create-db: ## Cria o arquivo .db do sqlite dentro do container
	docker-compose run app flask db migrate && flask db upgrade

container-down: ## Para e remove os containers da aplicacao
	docker-compose down

container-tail-logs: ## Acompanha os logs do container da aplicacao
	docker-compose logs -f $(container)

container-build-apidocs: ## Gera documentacao com base no arquivo das especificacoes do API Blueprint
	docker run -it --rm -v $(pwd):/application -w /application markteam/docker-aglio:latest aglio -i ./application/app/docs/api-blueprint-sample.apib --theme-full-width --no-theme-condense -o ./application/app/templates/apidocs/index.html
