# Nome do ambiente virtual
VENV := venv

# Caminho do interpretador Python dentro do ambiente virtual
PYTHON := $(VENV)/bin/python

# Instalação do ambiente virtual e dependências
install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Ambiente configurado com sucesso! ✅"

# Atualizar dependências e salvar no requirements.txt
update-deps:
	$(PYTHON) -m pip install --upgrade -r requirements.txt
	$(PYTHON) -m pip freeze > requirements.txt
	@echo "Dependências atualizadas! 🔄"

# Recriar o ambiente virtual
reinstall: clean install
	@echo "Ambiente virtual recriado com sucesso! 🔄"

# Ativar o ambiente virtual (para Linux/Mac)
activate:
	@echo "Para ativar o ambiente, execute: source $(VENV)/bin/activate"

# Rodar a aplicação
run:
	$(PYTHON) src/app.py

# Executar os testes
test:
	pytest -xvs --cov=src --cov-report=term-missing
	$(PYTHON) -m unittest discover -s tests

# Verificar a formatação do código com Black
format:
	$(PYTHON) -m black src/ tests/
	isort src/ tests/
	@echo "Código formatado com sucesso! ✨"

# Verificar qualidade do código com linters
lint:
	flake8 src/ tests/
	pylint src/
	mypy src/

# Rodar todos os checks automaticamente
check: lint test
	@echo "Todos os checks passaram! ✅"

# Remover arquivos desnecessários
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf $(VENV)
	@echo "Arquivos temporários removidos! 🧹"
