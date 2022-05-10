from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser



def scrape():
    
    # Step 1:  Scrape the Mars news site for the latest news title and paragraph text
    browser = init_browser()
    url = 'https://redplanetscience.com'
    browser.visit(url)

    mars_dict = {}

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Extract the latest news title
    news_title = soup.find('div', class_='content_title').get_text()
    # Extract the latest paragraph
    news_p = soup.find('div', class_ = 'article_teaser_body').get_text()

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

  

    # Step 2:  Use splinter to navigate the JPL Mars Space Images site for images
    url_jpl = 'https://spaceimages-mars.com'
    browser.visit(url_jpl)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Use splinter to click button "FULL IMAGE"
    browser.links.find_by_partial_text('FULL').click()
    # Extract image src data
    image_src = soup.find('img', class_ = 'headerimage fade-in')['src']
    # Format resulting url
    featured_image_url = url_jpl + "/" + image_src

    mars_dict['featured_image_url'] = featured_image_url

    # Step 3:  Mars Facts to scrape table and convert to HTML table string
    url_facts = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url_facts)
    type(tables)
    df = tables[0]
    df.iloc[0,0] = "Variable"
    html_table = df.to_html()
    html_table

    # Step 4:  Mars Hemispheres to scrape image urls and titles
    url_hemi = 'https://marshemispheres.com'
    browser.visit(url_hemi)
    
    hemisphere_image_urls = []

    for x in range (4):
        url_hemi = 'https://marshemispheres.com/'
        browser.visit(url_hemi)
        image = browser.find_by_tag('h3')
        time.sleep(5)
        image[x].click()
        html1 = browser.html
        soup = BeautifulSoup(html1, 'html.parser')
        url1 = soup.find('img', class_='wide-image')['src']
        title = soup.find('h2', class_ = 'title').get_text()

        dict = {'title': title, 'image_url': url_hemi + url1}
        hemisphere_image_urls.append(dict)

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit

    return mars_dict