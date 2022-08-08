from pprint import pprint

import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = "https://tonarinoyj.jp/series"
manga_title = "ワンパンマン"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
manga_title_tag = soup.select_one(f"h4:-soup-contains('{manga_title}')")
manga_container = manga_title_tag.parent.parent
manga_url = manga_container.select_one(".episode-link-container .link-latest a")["href"]

driver.get(manga_url)
latest_manga_title = driver.title

driver.quit()

print(f"{latest_manga_title} : {manga_url}")
