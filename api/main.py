from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="API de Consulta de Livros",
    description="Uma API para consultar dados de livros extraídos do site books.toscrape.com",
    version="1.0.0"
)

# Carrega os dados dos livros do arquivo CSV
try:
    df_books = pd.read_csv("data/books.csv")
    # Adiciona um ID único para cada livro
    df_books["id"] = range(len(df_books))
except FileNotFoundError:
    print("Arquivo data/books.csv não encontrado. Execute o script de scraping primeiro.")
    df_books = pd.DataFrame() # Dataframe vazio para evitar erros na inicialização

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

# --- Modelos de Dados (Pydantic) ---

class Book(BaseModel):
    id: int
    title: str
    price: str
    rating: str
    availability: str
    category: str
    image_url: str
    book_url: str

# --- Endpoints da API ---

@app.get("/api/v1/books", response_model=List[Book], tags=["Livros"])
def get_all_books():
    """
    Lista todos os livros disponíveis na base de dados.
    """
    if df_books.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")
    return df_books.to_dict(orient="records")

@app.get("/api/v1/books/{book_id}", response_model=Book, tags=["Livros"])
def get_book_by_id(book_id: int):
    """
    Retorna os detalhes de um livro específico pelo seu ID.
    """
    book = df_books[df_books["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    return book.to_dict(orient="records")[0]

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
