from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.example.com/")
