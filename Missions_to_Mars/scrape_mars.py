from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Mars News
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    
    # Find the latest News Title
    news_title = soup.find_all('div', class_="content_title")[1].text.strip()
   
    # Find the latest Paragraph text of the latest News Title
    news_p = soup.find('div', class_="article_teaser_body").text

    
    # Visit NASA JPL Website
    imageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imageurl)

    # Give the page time to load
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    imageSoup = bs(html, "html.parser")

    # Find the JPL Featured Space Image URL 

    # Click the full image link
    browser.click_link_by_id("full_image")

    # Give the page time to load
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    imagesoup = bs(html, "html.parser")

    # Find the partial image URL
    url = "https://www.jpl.nasa.gov"
    img_url = imagesoup.find("img", class_="fancybox-image")["src"]

    # Create the full image URL
    featured_image_url = url + img_url





    # Visit Mars Facts Website
    factsurl = 'https://space-facts.com/mars/'
    browser.visit(factsurl)

    # Give the page time to load
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    factSoup = bs(html, "html.parser")

    # Use Pandas to read the facts table to HTML
    factstable = pd.read_html(factsurl)
    factstable[0]

    # Use Panda's to transfer the HTML into a DataFrame
    factsdf = factstable[0]
    factsdf.columns = ['Description' , 'Facts']
    factsdf = factsdf.set_index('Description')

    # Use Pandas to convert the data to a HTML table string
    html_table = factsdf.to_html()
    html_table

    # Visit USGS Astrogeology Website
    astrogeologyurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeologyurl)

    # Give the page time to load
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    USGSSoup = bs(html, "html.parser")

    # Create an empty list to store each of the titles 
    titles = []

    # Create an empty list to store each of the URLs 
    URLs = []

    # Create an empty list to store each of the titles and URLs
    astrogeology_list = []

    # Find the titles of each hemisphere
    hemispheres = USGSSoup.find_all("h3")
    hemispheres
    for hemisphere in hemispheres:
        titles.append(hemisphere.text)


    for title in titles:
        # Visit USGS Astrogeology Website
        astrogeologyurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(astrogeologyurl)
    
        # Give the page time to load
        time.sleep(3)

        # Click each image URL
        browser.click_link_by_partial_text(title)

        # Scrape each page into Soup
        html = browser.html
        USGSImgSoup = bs(html, "html.parser")
        image_url = USGSImgSoup.find_all("li")[0].a["href"]
        URLs.append(image_url)

        # Create a dictionary of title and url
        astrogeology_dict = {"title":title, "image_url":image_url}
        # add this dictionary to the list
        astrogeology_list.append(astrogeology_dict)


    # Store data in a dictionary
    
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "html_table": html_table,
        "title": title,
        "image_url":image_url,
        "hemispheres": astrogeology_list
    }


    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_dict

