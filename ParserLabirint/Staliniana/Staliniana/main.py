import requests
from bs4 import BeautifulSoup
import time
import json

def ParsLabirint():
    page = 1
    url = f"https://www.labirint.ru/search/cnfkbybfyf/?stype=0"
    heders ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
    while(True):
            book_helf = 0
            url = f"https://www.labirint.ru/search/cnfkbybfyf/?stype=0"

            #Копируем страницу с нужными результатами.
            src = requests.get(url, heders).text
            site = open(f"site_HTML_{page}.txt", 'w')
            site.write(src)
            site.close()

            #Выбираем сылки на книги.
            site = open(f'site_HTML_{page}.txt', 'r')
            src = site.read()
            soup = BeautifulSoup(src, "lxml")
            all_books_helf = soup.find_all("a",class_= "cover")
            books_href=[]
            hrefs = open("hrefs.txt", 'w')
            for book in all_books_helf:
                try:
                    hrefs.write("https://www.labirint.ru"+book.get("href")+"\n")
                except:
                    break
            hrefs.close()

            #Создаем сводку по ссылкам.
            hrefs = open("hrefs.txt", "r")
            hrefs_to_books = hrefs.readlines()
            for hrefs_to_book in hrefs_to_books:
                Books(hrefs_to_book)
                time.sleep(10)
                book_helf = book_helf + 1

            page = page + 1
            time.sleep(10)
            if (len(soup.find_all(class_="card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2")) == 0 ):
                break
            else:
                if (len(soup.find_all( class_="card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2")) == book_helf):
                    break

def Books(url):
    print(url.strip())
    info_book = []

    src = requests.get(url.strip()).text

    book_HTML = open("book_HTML.txt","w")
    book_HTML.write(src)
    book_HTML.close()

    book_HTML = open("book_HTML.txt","r")
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
    with open(f"Книги по Сталиниане.json", "a", encoding="utf-8") as file:
        json.dump(info_book, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    ParsLabirint()


