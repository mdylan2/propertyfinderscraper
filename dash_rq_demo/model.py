# Importing stuff
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
from urllib.parse import urlencode
import math

# Scraping Class
class scraper:
    # Initializing the class
    def __init__(self, c, t, rp):
        self.base = "https://www.propertyfinder.ae/en/search/?"
        self.c = c
        self.t = t
        self.rp = rp
        self.dictionary = {"c": self.c, "t": self.t, "rp": self.rp}
    
    # Generating the URL
    def generate_url(self, **kwargs):
        self.dictionary['page'] = dict(kwargs).pop("page")
        return self.base + urlencode(self.dictionary)
    
    # Get the content from a URL
    def connect_to_page(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.content, features="html.parser")
    
    # Calculate number of pages
    def count_all_pages(self):
        url = self.generate_url(page = 1)
        soup = self.connect_to_page(url)
        num_of_results = soup.find("div", {"data-qs": "search-results-count"}).text
        pages = math.ceil(int(num_of_results.strip()[:-8])/25)
        self.all_pages = tuple(i for i in range(1, pages + 1))
    
    # Scrape one pages
    def scrape_page(self, page_number): 
        url = self.generate_url(page = page_number)
        soup = self.connect_to_page(url)

        main_stuff = soup.findAll("div", {"class": "card__content"})

        title_list = []
        location_list = []
        price_list = []
        type_list = []
        bedroom_list = []
        bathroom_list = []
        area_list = []

        for ele in main_stuff:
            title_list.append(ele.find("h2", {"class": "card__title card__title-link"}).text)
            location_list.append(ele.find("p", {"class": "card__location"}).text)
            price_list.append(ele.find("span", {"class": "card__price-value"}).text)
            type_list.append(ele.find("p", {"class": "card__property-amenity card__property-amenity--property-type"}).text)

            try:
                bedroom_list.append(ele.find("p", {"class": "card__property-amenity card__property-amenity--bedrooms"}).text)
            except:
                bedroom_list.append("N/A")

            try:
                bathroom_list.append(ele.find("p", {"class": "card__property-amenity card__property-amenity--bathrooms"}).text)
            except:
                bathroom_list.append("N/A")   
            try:
                area_list.append(ele.find("p", {"class": "card__property-amenity card__property-amenity--area"}).text)      
            except:
                area_list.append("N/A")
        
        return title_list, location_list, price_list, type_list, bedroom_list, bathroom_list, area_list        