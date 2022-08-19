import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from libs import common
from libs.parser.providers import JumpplusParser, ShosetsuParser, TonarinoyjParser


class WebDriver:
    def __init__(self, headless: bool = True) -> None:
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # 待機時間の指定
        self.wait = WebDriverWait(self.driver, 20)

    def parse_ongoing_titles_in_tonarinoyj(self) -> dict[str, str]:
        self.get(common.PROVIDER_URLS["tonarinoyj"])
        parser = TonarinoyjParser(self.current_page_source)
        return parser.parse_ongoing_titles()

    def parse_latest_episode_url_in_jumpplus(self, first_episode_url: str) -> str:
        self.get(first_episode_url)

        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a.series-episode-list-container"))
        )
        parser = JumpplusParser(self.current_page_source)
        return parser.parse_latest_episode_url()

    def parse_tracking_title_in_shosetsu(self, novel_code: str) -> tuple[int, str]:
        url = common.PROVIDER_URLS["shosetsu"] + novel_code
        self.get(url)

        parser = ShosetsuParser(self.current_page_source)
        return parser.parse_latest_episode_number_and_title()

    def get(self, url: str) -> None:
        self.driver.get(url)

    def quit(self) -> None:
        self.driver.quit()

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def current_page_source(self) -> str:
        return self.driver.page_source

    @property
    def current_title(self) -> str:
        return self.driver.title
