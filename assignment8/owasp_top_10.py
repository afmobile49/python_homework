# Task 6: Scrape the OWASP Top 10 using Selenium and XPath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


driver = webdriver.Chrome()


# Task 6 - Start from the exact OWASP page specified in the assignment
url = "https://owasp.org/www-project-top-ten/"

driver.get(url)


# The OWASP project page now links to the current Top Ten release.
# Find that link using XPath and follow it.
current_release_link = WebDriverWait(driver, 15).until(
    lambda d: d.find_element(
        By.XPATH,
        "//a[contains(normalize-space(.), 'OWASP Top Ten 2025')]"
    )
)

current_release_url = current_release_link.get_attribute("href")

print("Current OWASP Top Ten page:", current_release_url)

driver.get(current_release_url)


# Task 6 - Find the 10 vulnerability links using XPath
vulnerability_xpath = (
    "//a[starts-with(normalize-space(.), 'A') "
    "and contains(normalize-space(.), ':2025 -')]"
)

WebDriverWait(driver, 15).until(
    lambda d: len(
        d.find_elements(
            By.XPATH,
            vulnerability_xpath
        )
    ) >= 10
)

vulnerability_elements = driver.find_elements(
    By.XPATH,
    vulnerability_xpath
)


# Task 6 - Store each vulnerability title and href in a dictionary
results = []

for vulnerability in vulnerability_elements:

    title = vulnerability.text
    href = vulnerability.get_attribute("href")

    vulnerability_data = {
        "Title": title,
        "URL": href
    }

    results.append(vulnerability_data)


# Task 6 - Create and print the DataFrame
owasp_df = pd.DataFrame(results)

print(owasp_df)


# Task 6 - Save the results to CSV
owasp_df.to_csv(
    "owasp_top_10.csv",
    index=False
)


print(
    "\nNumber of OWASP vulnerabilities found:",
    len(results)
)

print("File created: owasp_top_10.csv")


driver.quit()