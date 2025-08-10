from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional, Dict, Any

# Importa as funções de insights
from api.insights import (
    get_stats_overview,
    get_stats_by_category,
    get_top_rated_books,
    get_books_in_price_range
)

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Livros",
    description="Uma API para consultar dados de livros extraídos do site books.toscrape.com",
    version="1.0.0"
)

# Função para pré-processar os dados carregados do CSV
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e transforma os dados do DataFrame."""
    # 1. Limpar e converter a coluna de preço
    df['price'] = df['price'].replace({r'[£]': ''}, regex=True).astype(float)

    # 2. Mapear e converter a coluna de rating
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    # Assegura que a coluna é string antes de mapear para evitar erros
    df['rating'] = df['rating'].astype(str).map(rating_map)

    # 3. Lidar com possíveis valores NaN após a conversão de forma robusta
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)

    # 4. Adicionar um ID único
    df["id"] = range(len(df))
    return df

# Carrega e pré-processa os dados dos livros
try:
    df_books_raw = pd.read_csv("data/books.csv")
    df_books = preprocess_data(df_books_raw)
except FileNotFoundError:
    print("Arquivo data/books.csv não encontrado. Execute o script de scraping primeiro.")
    df_books = pd.DataFrame() # Dataframe vazio para evitar erros na inicialização

# --- Modelos de Dados (Pydantic) ---

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    availability: str
    category: str
    image_url: str
    book_url: str

class StatsOverview(BaseModel):
    total_books: int
    average_price: float
    rating_distribution: Dict[str, int]

class CategoryStat(BaseModel):
    category: str
    total_books: int
    average_price: float

# --- Endpoints da API ---

@app.get("/api/v1/health", tags=["Status"])
def health_check():
    """
    Verifica o status da API e a disponibilidade dos dados.
    """
    if not df_books.empty:
        return {"status": "ok", "message": "API está funcional e os dados estão carregados."}
    else:
        raise HTTPException(status_code=503, detail="Serviço indisponível. Os dados dos livros não foram carregados.")

@app.get("/api/v1/books", response_model=List[Book], tags=["Livros"])
def get_all_books():
    """
    Lista todos os livros disponíveis na base de dados.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")
    return df_books.to_dict(orient="records")

@app.get("/api/v1/books/search", response_model=List[Book], tags=["Livros"])
def search_books(title: Optional[str] = None, category: Optional[str] = None):
    """
    Busca livros por título e/ou categoria.
    Pelo menos um dos parâmetros (título ou categoria) deve ser fornecido.
    """
    if not title and not category:
        raise HTTPException(status_code=400, detail="Forneça um título ou uma categoria para a busca.")

    results = df_books.copy()
    if title:
        results = results[results["title"].str.contains(title, case=False, na=False)]
    if category:
        results = results[results["category"].str.contains(category, case=False, na=False)]

    if results.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado para os critérios de busca.")
    return results.to_dict(orient="records")

@app.get("/api/v1/categories", response_model=List[str], tags=["Categorias"])
def get_all_categories():
    """
    Lista todas as categorias de livros únicas disponíveis.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Nenhuma categoria encontrada.")
    return sorted(df_books["category"].unique().tolist())

@app.get("/api/v1/books/top-rated", response_model=List[Book], tags=["Livros"])
def get_top_rated():
    """
    Lista os livros com a melhor avaliação (5 estrelas).
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Dados de livros não disponíveis.")
    return get_top_rated_books(df_books.copy())

@app.get("/api/v1/books/price-range", response_model=List[Book], tags=["Livros"])
def get_price_range(min_price: float, max_price: float):
    """
    Filtra livros dentro de uma faixa de preço específica.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Dados de livros não disponíveis.")
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="O preço mínimo não pode ser maior que o preço máximo.")
    return get_books_in_price_range(df_books.copy(), min_price, max_price)

@app.get("/api/v1/books/{book_id}", response_model=Book, tags=["Livros"])
def get_book_by_id(book_id: int):
    """
    Retorna os detalhes de um livro específico pelo seu ID.
    """
    book = df_books[df_books["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    return book.to_dict(orient="records")[0]

# --- Endpoints de Insights ---

@app.get("/api/v1/stats/overview", response_model=StatsOverview, tags=["Estatísticas"])
def get_overview_stats():
    """
    Retorna estatísticas gerais da coleção: total de livros, preço médio e distribuição de ratings.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Dados de livros não disponíveis.")
    return get_stats_overview(df_books.copy())

@app.get("/api/v1/stats/categories", response_model=List[CategoryStat], tags=["Estatísticas"])
def get_category_stats():
    """
    Retorna estatísticas por categoria: quantidade de livros e preço médio.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Dados de livros não disponíveis.")
    return get_stats_by_category(df_books.copy())
