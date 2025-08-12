# Plano Arquitetural - API de Consulta de Livros

Este documento detalha a arquitetura do projeto da API de consulta de livros, desde a ingestão de dados até o consumo final, com foco em escalabilidade e integração com Machine Learning.

## 1. Visão Geral do Pipeline de Dados

O pipeline de dados foi desenhado para ser modular e escalável, seguindo as etapas abaixo:

**Ingestão → Processamento/Armazenamento → API → Consumo**

1.  **Ingestão (Web Scraping):**
    *   Um script Python (`scraper.py`) será responsável por extrair os dados do site [https://books.toscrape.com/](https://books.toscrape.com/).
    *   O script navegará por todas as páginas e categorias para coletar informações de cada livro.
    *   **Ferramentas:** `requests` e `BeautifulSoup`.

2.  **Processamento e Armazenamento:**
    *   Os dados extraídos (título, preço, avaliação, disponibilidade, categoria, imagem) serão limpos e estruturados.
    *   Inicialmente, os dados serão armazenados em um arquivo `data/books.csv` para simplicidade e portabilidade.
    *   **Escalabilidade:** Para um ambiente de produção maior, este passo pode ser substituído por um banco de dados NoSQL (como MongoDB) ou um Data Warehouse (como BigQuery), sem a necessidade de grandes alterações no restante do pipeline.

3.  **Disponibilização (API RESTful):**
    *   Uma API RESTful, desenvolvida com **FastAPI**, servirá os dados.
    *   O FastAPI foi escolhido por sua alta performance, documentação automática (Swagger UI) e sintaxe moderna com tipos.
    *   A API lerá os dados do arquivo CSV (ou do banco de dados) e os exporá através de endpoints bem definidos.

4.  **Consumo:**
    *   A API poderá ser consumida por diversas aplicações:
        *   **Cientistas de Dados:** Para análise exploratória e treinamento de modelos de recomendação.
        *   **Aplicações Web/Mobile:** Para exibir catálogos de livros.
        *   **Outros Serviços:** Para integrar com sistemas de recomendação existentes.

## 2. Arquitetura da Solução

A arquitetura foi atualizada para incluir módulos de autenticação e geração de insights, tornando-a mais robusta e preparada para cenários de produção.

*   **Módulo de Scraping (`scripts/`):** Responsável pela extração de dados. Sem alterações.
*   **Módulo de Dados (`data/`):** Armazena os dados extraídos. Sem alterações.
*   **Módulo da API (`api/`):**
    *   **`main.py`:** Orquestra as rotas e a lógica principal.
    *   **`insights.py`:** Contém a lógica para gerar estatísticas e insights a partir dos dados dos livros.
    *   **`auth/`:** Submódulo que implementa a autenticação de usuários via JWT, protegendo endpoints sensíveis.



## 3. Cenário de Uso para Ciência de Dados e Machine Learning

Um cientista de dados pode utilizar a API para obter um dataset limpo e estruturado para criar um sistema de recomendação.

**Exemplo de Workflow:**

1.  **Autenticação:** O consumidor obtém um token de acesso via `POST /api/v1/auth/login`.
2.  **Coleta de Dados:** Utiliza o token para acessar endpoints protegidos, como `GET /api/v1/books`, para obter os dados.
3.  **Análise Exploratória:** Consome os endpoints do módulo de insights para entender os dados:
    *   `GET /api/v1/stats/overview`: Visão geral das métricas.
    *   `GET /api/v1/stats/categories`: Distribuição de livros por categoria.
    *   `GET /api/v1/books/top-rated`: Livros com melhores avaliações.
4.  **Pré-processamento:** Utiliza os dados obtidos para criar features para o modelo.
4.  **Treinamento do Modelo:** Treina um modelo de recomendação (ex: filtragem colaborativa ou baseada em conteúdo) com os dados.
5.  **Integração:** Após o treinamento, o modelo pode ser integrado à API ou a um serviço separado que consome a API para obter dados de novos livros.

## 4. Plano de Integração com Modelos de ML

A API foi estendida com endpoints de autenticação e insights:

### Endpoints de Autenticação (`/api/v1/auth`)

*   `POST /login`: Autentica um usuário e retorna um token JWT.
*   `POST /refresh`: Atualiza um token de acesso expirado.

### Endpoints de Insights e Estatísticas

*   `GET /api/v1/stats/overview`: Retorna uma visão geral dos dados, como número total de livros e preço médio.
*   `GET /api/v1/stats/categories`: Retorna estatísticas de livros por categoria.
*   `GET /api/v1/books/top-rated`: Lista os livros com a maior avaliação.
*   `GET /api/v1/books/price-range`: Filtra livros por uma faixa de preço.

Essa arquitetura permite que o pipeline de dados e a API de serviço evoluam de forma independente do ciclo de vida dos modelos de Machine Learning, com uma camada de segurança e análise de dados aprimorada.