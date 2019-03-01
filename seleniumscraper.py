import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup

from scraper import Scraper

class SeleniumScraper(object):

	#url - the url you want to scrape - eg. persian recipe
	def __init__(self,url, parser = "html.parser"):

		#get the url
		r = requests.get(url)
		html = r.text

		#this is the url which we will be scraping for all the urls
		self.url_scrapped = url
		#these are all the set of urls we need to scrape through the 
		self.to_scrape = set()

        

		
	#this scrapes the webpage for all the urls and appends it to the instance variable to_scrape
	#This must be called before calling function get_urls_to_be_scraped
	def scrape_urls(self):
		path = "./chromedriver"
		page = "https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/"
		options = Options()
        # options.add_argument('--start-fullscreen')
        # options.add_argument('--disable-infobars')

		driver = webdriver.Chrome(chrome_options=options, executable_path=path)
		driver.get(page)

		

		for i in range(6):
			res = driver.execute_script("return document.documentElement.outerHTML")
			self.soup = BeautifulSoup(res, features="html.parser")
			#instantiate the scraper object 
			urls_scrapped = self.get_urls()

			for ref in urls_scrapped:
				self.to_scrape.add(ref)


			time.sleep(1)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			print("THE SET ",self.to_scrape)


	#This returns the list of all the urls that need to be scraped
	def get_urls_to_be_scraped(self):

		return self.to_scrape
		


	#this method is used in the selenium scraper
	def get_urls(self):
		urls = self.soup.find_all("a",class_="ng-isolate-scope")

		
		ref = []

		if urls is not None:

			for u in urls:

				if u is not None:

					if "href" in u:

						ref.append(u['href'])
		print(ref)
		return ref