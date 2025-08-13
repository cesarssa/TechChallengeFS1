# API Pública para Consulta de Livros

Este projeto consiste em um pipeline de dados e uma API RESTful para consultar informações de livros extraídas do site [books.toscrape.com](http://books.toscrape.com/). O objetivo é fornecer uma fonte de dados estruturada para cientistas de dados e serviços de recomendação.

## Arquitetura

A arquitetura do projeto é dividida em três componentes principais:

1.  **Web Scraper (`scripts/scraper.py`):** Um script Python que navega pelo site `books.toscrape.com`, extrai os dados de todos os livros e os salva em um arquivo `data/books.csv`.
2.  **Armazenamento (`data/books.csv`):** Um arquivo CSV que armazena os dados extraídos, servindo como nossa base de dados local.
3.  **API RESTful (`api/`):** Uma API desenvolvida com FastAPI que expõe os dados através de endpoints HTTP. A API agora inclui:
    *   **Módulo de Insights (`api/insights.py`):** Funções para extrair estatísticas e insights dos dados.
    *   **Módulo de Autenticação (`api/auth/`):** Sistema de autenticação de usuários com JWT para proteger rotas.

Para mais detalhes, consulte o documento [ARQUITETURA.md](ARQUITETURA.md).

## Instalação e Configuração

O projeto utiliza `conda` para gerenciamento de ambiente.

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie o ambiente Conda:**
    ```bash
    conda create --name tech_challenge python=3.13 -y
    ```

3.  **Ative o ambiente:**
    ```bash
    conda activate tech_challenge
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Instruções para Execução

1.  **Execute o Web Scraper:**
    Para popular a base de dados, execute o script de scraping. Este comando irá criar o arquivo `data/books.csv`.
    ```bash
    python scripts/scraper.py
    ```

2.  **Inicie a API:**
    Para iniciar o servidor da API localmente, use o `uvicorn`.
    ```bash
    uvicorn api.main:app --reload
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

## Documentação da API (Swagger)

A documentação interativa da API (Swagger UI) é gerada automaticamente pelo FastAPI e pode ser acessada em:

**`http://127.0.0.1:8000/docs`**

### Rotas da API

#### Health Check

*   `GET /api/v1/health`
    *   **Descrição:** Verifica o status da API.
    *   **Resposta (200):**
        ```json
        {
          "status": "ok",
          "message": "API está funcional e os dados estão carregados."
        }
        ```

#### Livros

*   `GET /api/v1/books`
    *   **Descrição:** Lista todos os livros.
    *   **Resposta (200):**
        ```json
        [
          {
            "id": 0,
            "title": "A Light in the Attic",
            "price": "£51.77",
            "rating": "Three",
            "availability": "In stock (22 available)",
            "category": "Poetry",
            "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
            "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
          }
        ]
        ```

*   `GET /api/v1/books/{id}`
    *   **Descrição:** Retorna um livro específico pelo ID.
    *   **Exemplo:** `GET /api/v1/books/0`
    *   **Resposta (200):** (Semelhante ao item da lista acima)

*   `GET /api/v1/books/search?title={title}&category={category}`
    *   **Descrição:** Busca livros por título e/ou categoria.
    *   **Exemplo:** `GET /api/v1/books/search?category=Poetry`
    *   **Resposta (200):** (Lista de livros que correspondem à busca)

#### Categorias

*   `GET /api/v1/categories`
    *   **Descrição:** Lista todas as categorias disponíveis.
    *   **Resposta (200):**
        ```json
        [
          "Add a comment",
          "Art",
          "Autobiography",
          "Biography",
          "Business"
        ]
        ```

#### Estatísticas e Insights

*   `GET /api/v1/stats/overview`
    *   **Descrição:** Retorna uma visão geral dos dados, como o número total de livros, o preço médio e a contagem de livros por avaliação.
*   `GET /api/v1/stats/categories`
    *   **Descrição:** Retorna estatísticas detalhadas por categoria, incluindo o número de livros e o preço médio.
*   `GET /api/v1/books/top-rated`
    *   **Descrição:** Lista os livros com a avaliação mais alta (cinco estrelas).
*   `GET /api/v1/books/price-range?min_price={min}&max_price={max}`
    *   **Descrição:** Filtra livros que estão dentro de uma faixa de preço especificada.

#### Autenticação

*   `POST /api/v1/auth/login`
    *   **Descrição:** Autentica um usuário com `username` e `password` e retorna um `access_token` JWT.
*   `POST /api/v1/auth/refresh`
    *   **Descrição:** Recebe um `access_token` válido (mesmo que expirado) e retorna um novo `access_token`.

## Deploy

O projeto está configurado para deploy em plataformas como Heroku ou Render usando o `Procfile` e o `requirements.txt`.

A aplicação está disponível em produção em:
[https://techchallengefs1.onrender.com/docs](https://techchallengefs1.onrender.com/docs)
