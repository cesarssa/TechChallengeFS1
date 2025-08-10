# -*- coding: utf-8 -*-
"""
Módulo para funções de cálculo de estatísticas e insights da API.
"""
import pandas as pd
from typing import List, Dict, Any

def get_stats_overview(books_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula estatísticas gerais da coleção de livros.

    Args:
        books_df: DataFrame com os dados dos livros.

    Returns:
        Dicionário com as estatísticas.
    """
    total_books = len(books_df)
    average_price = books_df['price'].mean()
    
    rating_distribution = books_df['rating'].value_counts().to_dict()

    return {
        "total_books": total_books,
        "average_price": round(average_price, 2),
        "rating_distribution": {f"{k}_stars": v for k, v in rating_distribution.items()}
    }
# Funções de insights serão adicionadas aqui.

def get_stats_by_category(books_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula estatísticas de livros agrupadas por categoria.

    Args:
        books_df: DataFrame com os dados dos livros.

    Returns:
        Dicionário com estatísticas por categoria.
    """
    category_stats = books_df.groupby('category').agg(
        total_books=('title', 'count'),
        average_price=('price', 'mean')
    ).reset_index()

    # Arredonda o preço médio para 2 casas decimais
    category_stats['average_price'] = category_stats['average_price'].round(2)

    return category_stats.to_dict(orient='records')

def get_top_rated_books(books_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Filtra os livros com a avaliação mais alta (5 estrelas).

    Args:
        books_df: DataFrame com os dados dos livros.

    Returns:
        Lista de dicionários com os livros de maior avaliação.
    """
    top_rated_df = books_df[books_df['rating'] == 5]
    # Conversão manual para garantir tipos compatíveis com JSON/Pydantic
    return [
        {
            "id": int(row.id),
            "title": str(row.title),
            "price": float(row.price),
            "rating": int(row.rating),
            "availability": str(row.availability),
            "category": str(row.category),
            "image_url": str(row.image_url),
            "book_url": str(row.book_url),
        }
        for row in top_rated_df.itertuples()
    ]

def get_books_in_price_range(books_df: pd.DataFrame, min_price: float, max_price: float) -> List[Dict[str, Any]]:
    """
    Filtra os livros dentro de uma faixa de preço.

    Args:
        books_df: DataFrame com os dados dos livros.
        min_price: Preço mínimo.
        max_price: Preço máximo.

    Returns:
        Lista de dicionários com os livros na faixa de preço.
    """
    filtered_df = books_df[
        (books_df['price'] >= min_price) & (books_df['price'] <= max_price)
    ]
    # Conversão manual para garantir tipos compatíveis com JSON/Pydantic
    return [
        {
            "id": int(row.id),
            "title": str(row.title),
            "price": float(row.price),
            "rating": int(row.rating),
            "availability": str(row.availability),
            "category": str(row.category),
            "image_url": str(row.image_url),
            "book_url": str(row.book_url),
        }
        for row in filtered_df.itertuples()
    ]