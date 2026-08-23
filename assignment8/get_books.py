# Task 3: Extract book data from the Durham County Library search results

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json

from selenium.webdriver.support.ui import WebDriverWait


try:
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
except Exception:
    print("WebDriver Manager could not download the driver.")
    print("Using Selenium Manager instead.")
    driver = webdriver.Chrome()

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

driver.get(url)

# Wait until all 20 search results on the first page are loaded
WebDriverWait(driver, 15).until(
    lambda d: len(
        d.find_elements(
            By.CSS_SELECTOR,
            "li.row.cp-search-result-item"
        )
    ) >= 20
)

book_entries = driver.find_elements(
    By.CSS_SELECTOR,
    "li.row.cp-search-result-item"
)

print("Number of results found:", len(book_entries))

results = []

for book in book_entries:
    title_element = book.find_element(
        By.CSS_SELECTOR,
        "span.title-content"
    )
    title = title_element.text

    author_elements = book.find_elements(
        By.CSS_SELECTOR,
        "a.author-link"
    )
    authors = []

    for author in author_elements:
        authors.append(author.text)

    author_text = "; ".join(authors)

    format_div = book.find_element(
        By.CSS_SELECTOR,
        "div.cp-format-info"
    )

    format_year_element = format_div.find_element(
        By.CSS_SELECTOR,
        "span.display-info-primary"
    )
    format_year = format_year_element.text

    book_data = {
        "Title": title,
        "Author": author_text,
        "Format-Year": format_year
    }

    results.append(book_data)


books_df = pd.DataFrame(results)

print(books_df)

# Task 4: Write the scraped data to CSV and JSON files

books_df.to_csv("get_books.csv", index=False)

with open("get_books.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, indent=4, ensure_ascii=False)

print("\nFiles created:")
print("get_books.csv")
print("get_books.json")

driver.quit()