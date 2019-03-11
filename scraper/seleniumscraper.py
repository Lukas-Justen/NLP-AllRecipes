import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumScraper(object):

    def __init__(self, url):
        self.url_scrapped = url
        self.to_scrape = set()

    def scrape_urls(self):
        path = "./chromedriver"
        options = Options()
        options.add_argument('--start-fullscreen')
        options.add_argument('--disable-infobars')

        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        driver.get(self.url_scrapped)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(self.to_scrape) <= 100:
            print(len(self.to_scrape))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            res = driver.execute_script("return document.documentElement.outerHTML")
            self.soup = BeautifulSoup(res, features="html.parser")

            btn = driver.find_element_by_id("btnMoreResults")
            if btn and btn.is_displayed():
                btn.click()
                time.sleep(2)
            urls_scrapped = self.get_urls()

            for ref in urls_scrapped:
                self.to_scrape.add(ref)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_urls_to_be_scraped(self):
        return self.to_scrape

    def get_urls(self):
        urls = self.soup.find_all("article", class_="fixed-recipe-card")
        urls_container = [u.find("div", class_="grid-card-image-container") for u in urls if u]
        urls_isolated = [u.find("a", class_="ng-isolate-scope") for u in urls_container if u]
        urls_isolated = [u for u in urls_isolated if u]
        urls_scope = [u.find("a", class_="ng-scope") for u in urls_container if u]
        urls_scope = [u for u in urls_scope if u]
        urls = urls_isolated + urls_scope

        ref = []
        for u in urls:
            ref.append(str(u['href']))

        return ref
