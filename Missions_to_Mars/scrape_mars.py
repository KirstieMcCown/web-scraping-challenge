# Import Dependancies 
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Define the browser to open and run the scraper
def init_browser():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# Define the scraper tool
def scrape():
    browser = init_browser()

    # Visit NASA Mars News Site
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)

    # Give the page time to load
    time.sleep(1)

# Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser') 


# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        news_title = result.find('a', target_="_self").text
        # Identify and return price of listing
        news_p = result.a.target.text

        # Print results only if title, price, and link are available
        if (news_title and news_p):
            print('-------------')
            print(title)
            print(news_p)
    except AttributeError as e:
        print(e)