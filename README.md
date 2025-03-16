# API de Manipulação e Conversão de Arquivos HTML

Esta API foi desenvolvida para ser utilizada localmente com o auxílio de ferramentas como **Postman** e **Insomnia**. Seu objetivo é permitir a leitura, edição e conversão de arquivos HTML para outros formatos, facilitando o processamento e transformação de conteúdo.

## Índice

- [Recursos Utilizados](#recursos-utilizados)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Autenticação](#autenticação)
  - [Exemplos de Requisição](#exemplos-de-requisição)
- [Endpoints](#endpoints)
  - [`GET /arquivos`](#get-arquivos)
  - [`POST /converter`](#post-converter)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Recursos Utilizados

- **Python** - Linguagem principal do projeto
- **Flask** - Framework web para roteamento
- **Requests** - Biblioteca para requisições HTTP
- **Pytest** - Framework de testes
- **Tkinter** ou **Kivy** - Interface gráfica para manipulação visual
- **OS e Shutil** - Manipulação de arquivos e diretórios

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/DiasPedroQA/UniBMark
   ```

2. **Acesse a pasta do projeto:**

   ```bash
   cd UniBMark
   ```

3. **Crie um ambiente virtual e ative-o:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

4. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a API:**

   ```bash
   python app.py
   ```

   A API estará disponível em `http://localhost:5000`.

## Uso

### Autenticação

Esta API não requer autenticação para ser utilizada localmente.

### Exemplos de Requisição

#### Listar arquivos na pasta `uploads/`

```bash
GET /arquivos
```

**Resposta:**

```json
{
  "arquivos": ["index.html", "sobre.html", "contato.html"]
}
```

#### Buscar o conteúdo de um arquivo

```bash
GET /arquivo/index.html
```

**Resposta:**

```json
{
  "nome": "index.html",
  "conteudo": "<html><head><title>Exemplo</title></head><body><h1>Exemplo</h1></body></html>"
}
```

#### Converter um arquivo HTML para JSON

```bash
POST /converter
Content-Type: application/json

{
  "arquivo": "index.html",
  "formato": "json"
}
```

**Resposta:**

```json
{
  "arquivo_original": "index.html",
  "formato": "json",
  "conteudo": {
    "titulo": "Exemplo",
    "corpo": "<h1>Exemplo</h1>"
  }
}
```

## Endpoints

### `GET /arquivos`

Lista todos os arquivos na pasta `uploads/`.

- **Resposta:**

  ```json
  {
    "arquivos": ["index.html", "sobre.html", "contato.html"]
  }
  ```

### `GET /arquivo/:nome`

Obtém o conteúdo de um arquivo HTML.

- **Parâmetro:** `:nome` - Nome do arquivo (exemplo: `index.html`)
- **Resposta:**

  ```json
  {
    "nome": "index.html",
    "conteudo": "<html><head><title>Exemplo</title></head><body><h1>Exemplo</h1></body></html>"
  }
  ```

### `POST /converter`

Converte um arquivo HTML para outro formato (JSON, TXT, CSV, etc.).

- **Requisição:**

  ```json
  {
    "arquivo": "index.html",
    "formato": "json"
  }
  ```

- **Resposta:**

  ```json
  {
    "arquivo_original": "index.html",
    "formato": "json",
    "conteudo": {
      "titulo": "Exemplo",
      "corpo": "<h1>Exemplo</h1>"
    }
  }
  ```

## Contribuição

Quer contribuir com esse projeto? Fique à vontade! Siga estas etapas:

1. **Fork o repositório** e clone para seu ambiente local:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-projeto.git
   ```

2. **Crie uma branch para sua funcionalidade ou correção:**

   ```bash
   git checkout -b minha-melhoria
   ```

3. **Implemente suas mudanças** e faça commits organizados:

   ```bash
   git commit -m "Adicionada nova funcionalidade X"
   ```

4. **Envie para o repositório remoto:**

   ```bash
   git push origin minha-melhoria
   ```

5. **Abra um Pull Request** e descreva suas modificações.

Sua contribuição é muito bem-vinda! 🚀

## Licença

Este projeto está licenciado sob a [Licença Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Contato

Caso tenha dúvidas, sugestões ou queira colaborar, entre em contato:

- **LinkedIn**: [linkedin.com/in/diaspedro-dev](https://www.linkedin.com/in/diaspedro-dev/)
- **E-mail**: [diaspedro.dev@gmail.com](mailto:diaspedro.dev@gmail.com)
