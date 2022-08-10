from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def find_latest_episode_url_and_title_from_title():
    url = "https://tonarinoyj.jp/series"
    manga_title = "ワンパンマン"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    title_element = driver.find_element("xpath", f"//h4[text()='{manga_title}']")
    manga_container = title_element.find_element("xpath", "../..")
    manga_container.find_element("css selector", ".episode-link-container .link-latest a").click()

    manga_url = driver.current_url
    latest_manga_title = driver.title

    driver.quit()

    print(f"{latest_manga_title} : {manga_url}")
