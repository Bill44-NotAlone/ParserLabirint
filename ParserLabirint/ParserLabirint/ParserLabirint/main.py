import json
import requests
from bs4 import BeautifulSoup
import time
import json
import os

def ParserLabirint(type,theme):
        page = 1
        heders ={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
        booktry = ""
        while(True):
                # type = search - поиск, series - серия, pubhouse - издательство, authors - автор.
                url = f"https://www.labirint.ru/search/{theme}/?stype=0&page={page}"
                if(type != "search"):
                    url = f"https://www.labirint.ru/{type}/{theme}/?page={page}"
                #Копируем страницу с нужными результатами.
                src = requests.get(url, heders).text
                try:
                    os.mkdir(theme)
                except:
                    pass
                site = open(f"{theme}/site_HTML_{page}.HTML", encoding="utf-8", mode='w')
                site.write(src)
                site.close()

                #Выбираем сылки на книги.
                site = open(f'{theme}/site_HTML_{page}.HTML', encoding="utf-8", mode='r')
                src = site.read()
                src = str(src)
                soup = BeautifulSoup(src, "lxml")
                all_books_helf = soup.find_all("a",class_= "cover")
                hrefs = open(f"{theme}/hrefs.txt", 'w')
                for book in all_books_helf:
                    try:
                        hrefs.write("https://www.labirint.ru"+book.get("href")+"\n")
                    except:
                        break
                hrefs.close()

                #Создаем сводку по ссылкам.
                hrefs = open(f"{theme}/hrefs.txt", "r")
                hrefs_to_books = hrefs.readlines()
                try:
                    booktry == hrefs_to_books[0]
                except:
                    return True
                booktry = hrefs_to_books[0]
                for hrefs_to_book in hrefs_to_books:
                    Books(hrefs_to_book, theme)

                page = page + 1
                time.sleep(10)

def Books(url, theme):
    print(url.strip())
    info_book = []

    src = requests.get(url.strip()).text

    book_HTML = open(f"{theme}/book_HTML.HTML",encoding="utf-8", mode="w")
    book_HTML.write(src)
    book_HTML.close()

    book_HTML = open(f"{theme}/book_HTML.HTML", encoding="utf-8", mode="r")
    soup = BeautifulSoup(book_HTML.read() , "lxml")

    #Информация о книге.
    book_url = url.strip()
    try: book_name = soup.find(class_ = "prodtitle").find("h1").text
    except: book_name = None
    try: book_author = soup.find(class_= "authors").find("a", class_ = "analytics-click-js").text
    except: book_author = None
    try: book_publisher = (soup.find(class_ = "publisher").text+" "+soup.find(class_ = "publisher").find("a", class_ = "analytics-click-js").text)[14::]
    except: book_publisher = None
    try: book_series = soup.find(class_="series").find("a", class_="analytics-click-js").text
    except: book_series = None
    try: book_buying = soup.find(class_="buying").find(class_="buying-priceold").find(class_="buying-priceold-val").find("span", class_="buying-priceold-val-number").text + "p."
    except:
        try: book_buying =soup.find(class_="buying").find(class_="buying-price missing-price").find("span",class_="buying-priceold-val").text
        except:
            try: #Не законченно
                book_buying =soup.find(class_="buying").find(class_="buying-price missing-price").find("span",class_="buying-priceold-val").text
            except: book_buying = None

    try: book_isbn = soup.find(class_="isbn").text
    except: book_isbn = None

    info_book.append(
            {
                "Название книги ": book_name,
                "Автор книги ": book_author,
                "Ссылка на книгу ":book_url,
                "Издательство ": book_publisher,
                "Серия ": book_series,
                "ISBN книги ": book_isbn
            }
        )
    with open(f"{theme}/Книги по {theme}.json", "a", encoding="utf-8") as file:
        json.dump(info_book, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    ParserLabirint("tyre", "theme/id")


