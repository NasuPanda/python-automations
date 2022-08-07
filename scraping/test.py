import pprint
import time

import bs4
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = "https://tonarinoyj.jp/series"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(2)

# find 系メソッドで取得出来る要素はページ操作のためのもの
elements = driver.find_elements("css selector", ".series-table-list")
pprint.pprint(elements)

soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
results = soup.find_all("h4")

pprint.pprint(results)

time.sleep(2)
driver.quit()
