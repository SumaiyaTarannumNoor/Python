import csv
from selenium import webdriver

driver = webdriver.Chrome()


driver.get("https://www.audible.com/search")

products = driver.find_elements(by='xpath', value='//li[contains(@class, "productListItem")]')

with open('audible_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Author', 'Duration'])

    for product in products:
        title = product.find_element(by='xpath', value='.//h3[contains(@class, "bc-heading")]').text
        author = product.find_element(by='xpath', value='.//li[contains(@class, "authorLabel")]').text
        duration = product.find_element(by='xpath', value='.//li[contains(@class, "runtimeLabel")]').text

        writer.writerow([title, author, duration])

        print(title)
        print(author)
        print(duration)

driver.quit()
