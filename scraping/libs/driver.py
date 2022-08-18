from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from libs import common
from libs.parser.providers import TonarinoyjParser


class WebDriver:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def parse_ongoing_titles_in_tonarinoyj(self) -> dict[str, str]:
        self.get(common.PROVIDER_URLS["tonarinoyj"])
        parser = TonarinoyjParser(self.current_page_source)
        return parser.parse_ongoing_titles()

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
