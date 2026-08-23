# Task 6: Scrape the OWASP Top 10 using Selenium and XPath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


driver = webdriver.Chrome()

url = "https://owasp.org/Top10/2025/"
driver.get(url)


# Wait until all 10 OWASP Top 10 links are loaded
WebDriverWait(driver, 15).until(
    lambda d: len(
        d.find_elements(
            By.XPATH,
            "//a[starts-with(normalize-space(.), 'A') and contains(normalize-space(.), ':2025 -')]"
        )
    ) >= 10
)


vulnerability_elements = driver.find_elements(
    By.XPATH,
    "//a[starts-with(normalize-space(.), 'A') and contains(normalize-space(.), ':2025 -')]"
)


results = []

for vulnerability in vulnerability_elements:
    title = vulnerability.text
    href = vulnerability.get_attribute("href")

    vulnerability_data = {
        "Title": title,
        "URL": href
    }

    results.append(vulnerability_data)


owasp_df = pd.DataFrame(results)

print(owasp_df)


owasp_df.to_csv(
    "owasp_top_10.csv",
    index=False
)


print("\nNumber of OWASP vulnerabilities found:", len(results))
print("File created: owasp_top_10.csv")


driver.quit()