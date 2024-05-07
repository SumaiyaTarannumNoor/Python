#Download Selenium web Driver from here - https://chromedriver.chromium.org/downloads
#Then visit here - 'https://googlechromelabs.github.io/chrome-for-testing/'
#Tutorial - https://www.youtube.com/watch?v=lM23Y1XFd2Q&t=235s

from selenium import webdriver

driver = webdriver.Chrome()


driver.get("https://www.audible.com/search")

products = driver.find_elements(by='xpath', value='//li[contains(@class, "productListItem")]')

for product in products:
    print(product.find_element(by='xpath', value='.//h3[contains(@class, "bc-heading")]').text)
    print(product.find_element(by='xpath', value='.//li[contains(@class, "authorLabel")]').text)
    print(product.find_element(by='xpath', value='.//li[contains(@class, "runtimeLabel")]').text)

driver.quit()
