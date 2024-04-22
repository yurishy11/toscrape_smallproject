import requests
from bs4 import BeautifulSoup

def scrape_choice(site_choice):
    if (not site_choice.isnumeric()):
        while (True):
            print("(1): Books\n(2): Quotes")
            choice = input("Choose an option again: ")
            if (choice.isnumeric()):
                site_choice = choice
                break

    if (int(site_choice) not in [1, 2]):
        print("Choose a number between the displayed ones...!")
    elif (int(site_choice) == 1):
        return "http://books.toscrape.com"
    else:
        return "http://quotes.toscrape.com"
            
def scrape_books(book_site):
    response = requests.get(book_site + "/catalogue/page-1.html")
    soup = BeautifulSoup(response.content, "html.parser")
    books_info = []

    try:
        for catalogue in range(1, 52):
            all_h3 = soup.find_all("h3")
            books_prices = soup.find_all("p", "price_color")

            for index, h3 in enumerate(all_h3):
                title = h3.next_element.attrs['title']
                price = books_prices[index].text
                books_info.append({"name": title, "price": price})
            
            response = requests.get(book_site + f"/catalogue/page-{catalogue}.html")
            soup = BeautifulSoup(response.content, "html.parser")
    except:
        print("Error during books scraping!")

    return books_info

def scrape_quotes(quotes_site):
    response = requests.get(quotes_site + "/page/1")
    soup = BeautifulSoup(response.content, "html.parser")
    quotes_info = []

    try:
        for catalogue in range(1,12):
            quotes_div = soup.find_all("span", {"class": "text"})
            author_small = soup.find_all("small", {"class": "author"})

            for index, quotes in enumerate(quotes_div):
                quotes_info.append({"author": author_small[index].text, "quote": quotes.text})
            
            response = requests.get(quotes_site + f"/page/{catalogue}")
            soup = BeautifulSoup(response.content, "html.parser")
    except:
        print("Error during quote scraping!")

    return quotes_info
    

if __name__ == "__main__":
    print("Webscrape Swiss Knife")
    print("(1): Books\n(2): Quotes")

    choice = input("Choose an option: ")
    if (int(choice) == 1):
        books_info = (scrape_books(scrape_choice(choice)))
        for book_info in books_info:
            print(f'Book Name: {book_info["name"]} \nBook Price: {book_info["price"]}')
            print("-" * 35)

    elif (int(choice) == 2):
        quotes_info = (scrape_quotes(scrape_choice(choice)))
        for quote in quotes_info:
            print(f'Author: {quote["author"]} \nQuote: {quote["quote"]}')
            print("-" * 35)
    else:
        print("Invalid Choice. Try Again!")
    
    