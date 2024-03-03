import Utility
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver


def analyse_websites(url):
    print("Analysing", url)

    # Use Selenium to get the page
    driver = webdriver.Firefox()  # Or whichever browser you prefer
    driver.get(url)
    # Get the page source and parse it with BeautifulSoup
    # Find all links
    # get all html code
    html = driver.page_source
    # parse html
    soup = BeautifulSoup(html, "html.parser")
    # write all html in utf-8
    with open("site.html", "w", encoding="utf-8") as file:
        print(soup.prettify())
        file.write(soup.prettify())

    a_llinks = soup.find_all('a', href=True)
    link_links = soup.find_all('link', href=True)

    links = a_llinks + link_links

    for link in links:
        if(link['href'].startswith("/")):
            link['href'] = url + link['href']
        print(link['href'])
        
        

    driver.quit()
    return
    # find any text or header or anything that is related to the buzzwords
    texts = soup.find_all(text=True)
    for text in texts:
        for buzzword in Utility.buzzwords:
            # check if the text contains any of the buzzwords
            if re.search(buzzword, text, re.IGNORECASE) and text not in Utility.texts:
                mainsite = url.split("/")[2]
                if mainsite not in Utility.erp_ai:
                    Utility.erp_ai[mainsite] = True
                    print("buzzword", buzzword)
                    Utility.texts.add(text)
                    print("text", text)

    for link in links:
        print("checking sublink", link['href'])
        for buzzword in Utility.buzzwords:
            if re.search(buzzword, link['href'], re.IGNORECASE) and link['href'] not in Utility.sidelinks:
                Utility.sidelinks.add(link['href'])
                print("sidelink", link['href'])
                analyse_websites([link['href']])
                break
