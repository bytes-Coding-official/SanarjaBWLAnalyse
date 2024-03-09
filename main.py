import Huggingface
import Scraper
import Utility


# with open("urls1.txt", "r") as file:
#     Utility.websites = file.readlines()
#     Utility.websites = [x.strip() for x in Utility.websites]
# 
# print(Utility.websites)

def main():
    for website in Utility.websites:
        mainsite = website.split("/")[2]
        if website not in Utility.url_tree:
            Utility.url_tree[mainsite] = Scraper.TreeNode(website)
        Scraper.analyse_websites(website)

    print(Utility.url_texts)

    elements = []
    for key, item in Utility.url_texts.items():
        subject = key + "::" + item
        elements.append(subject)

    Huggingface.train_ai(elements)
