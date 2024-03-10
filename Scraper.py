import re

from bs4 import BeautifulSoup
from selenium import webdriver

import Utility


# BUZZword combinier




class TreeNode:
    def __init__(self, url, parent=None):
        self.url = url
        self.children = set()
        self.depth = 0
        self.parent = parent

        if parent is not None:
            self.depth = parent.depth + 1

    def get_children(self):
        return self.children

    def get_url(self):
        return self.url

    def get_parent(self):
        return self.parent

    def get_height(self):
        return self.depth


def analyse_websites(url, parent=None):
    mainsite = url.split("/")[2]

    node = TreeNode(url, parent)
    if parent is not None:
        parent.children.add(node)

    print("checking depth:", node.depth, "max depth:", Utility.max_depth)
    if node.depth > Utility.max_depth:
        print("limit exceeded")
        return

    print("Analysing:", url)
    # Use Selenium to get the page
    driver = webdriver.Firefox()  # Or whichever browser you prefer

    driver.get(url)
    # Get the page source and parse it with BeautifulSoup
    # get all html code
    html = driver.page_source
    # parse html
    soup = BeautifulSoup(html, "html.parser")
    # write all html in utf-8

    a_links = soup.find_all('a', href=True)
    link_links = soup.find_all('link', href=True)
    links = a_links + link_links

    # get all hrefs out of links
    links = [link['href'] for link in links if link['href'] != ""]
    driver.quit()
    # find any text or header or anything that is related to the buzzwords
    texts = soup.find_all(text=True)
    print("checking current site for texts:", url)
    found = False
    for text in texts:
        for buzzword in Utility.buzzwords:
            # check if the text contains any of the buzzwords
            if re.search(buzzword, text, re.IGNORECASE) and text not in Utility.url_texts:
                if mainsite not in Utility.erp_ai:
                    Utility.erp_ai[mainsite] = True
                    if mainsite not in Utility.url_texts:
                        Utility.url_texts[mainsite] = set()
                    Utility.url_texts[mainsite].add(text)
                    print("text found:", text)
                    found = True
    if not found:
        Utility.erp_ai[mainsite] = False
        print("no text found in site:", url)

    links = link_filter(links, url)
    for link in links:
        print("checking sublink", link)
        Utility.sidelinks.add(link)
        analyse_websites(link, node)
    if mainsite not in Utility.erp_ai:
        Utility.erp_ai[mainsite] = False


def link_filter(links, url=""):
    new_links = set()
    for link in links:
        if link.startswith("/"):
            link = url + link
        if link_checker(link, url):
            new_links.add(link)
    print("new links found:", new_links)
    return new_links


def link_checker(link, url=""):
    if not link.startswith("http"):
        # remove that link
        return False
        # if site doesnt start with url or starts with url but ends with .jpg .css .js
    if not link.startswith(url) or link.endswith(".jpg") or link.endswith(".png") or link.endswith(".css") or link.endswith(".js"):
        # remove that link
        return False
    if link in Utility.sidelinks or link in Utility.opened_urls:
        return False
    for buzzword in Utility.buzzwords:
        if link not in Utility.sidelinks and re.search(buzzword, link, re.IGNORECASE):
            return True
