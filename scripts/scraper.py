import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base do site
BASE_URL = "https://books.toscrape.com/"

def get_book_details(book_url):
    """
    Extrai os detalhes de um único livro.
    """
    try:
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1").text
        price = soup.find("p", class_="price_color").text
        rating = soup.find("p", class_="star-rating")["class"][1]
        availability = soup.find("p", class_="instock availability").text.strip()
        category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
        image_url = BASE_URL + soup.find("div", class_="item active").find("img")["src"].replace("../", "")

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category,
            "image_url": image_url,
            "book_url": book_url
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {book_url}: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar {book_url}: {e}")
        return None

def scrape_books():
    """
    Realiza o web scraping de todos os livros do site.
    """
    all_books = []
    url = f"{BASE_URL}catalogue/page-1.html"
    page_num = 1

    while True:
        print(f"Scraping página: {page_num}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            books_on_page = soup.find_all("article", class_="product_pod")
            if not books_on_page:
                break

            for book in books_on_page:
                book_relative_url = book.find("h3").find("a")["href"]
                book_full_url = f"{BASE_URL}catalogue/{book_relative_url.replace('../', '')}"
                book_details = get_book_details(book_full_url)
                if book_details:
                    all_books.append(book_details)
                time.sleep(0.1) # Pequeno delay para não sobrecarregar o servidor

            next_page = soup.find("li", class_="next")
            if next_page:
                next_page_url = next_page.find("a")["href"]
                url = f"{BASE_URL}catalogue/{next_page_url}"
                page_num += 1
            else:
                break

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página {url}: {e}")
            break
        except Exception as e:
            print(f"Erro ao processar a página {url}: {e}")
            break

    return all_books

if __name__ == "__main__":
    print("Iniciando o web scraping...")
    books_data = scrape_books()
    if books_data:
        df = pd.DataFrame(books_data)
        df.to_csv("data/books.csv", index=False)
        print(f"Scraping finalizado. {len(df)} livros foram salvos em data/books.csv")
    else:
        print("Nenhum livro foi extraído.")