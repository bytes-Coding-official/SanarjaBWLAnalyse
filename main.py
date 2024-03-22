import Scraper
import Utility
import chatgpt

DEBUG = True


def main():
    chatgpt.DEBUG = DEBUG
    Scraper.DEBUG = DEBUG
    for website in Utility.websites:
        main_site = website.split("/")[2]
        if website not in Utility.url_tree:
            Utility.url_tree[main_site] = Scraper.TreeNode(website)
        Scraper.analyse_websites(website)

    if DEBUG:
        print(Utility.url_texts)

    elements = []
    for key, item in Utility.url_texts.items():
        subject = "von Website/Unternehmen " + key + " haben wir Informationen: " + " ".join(item)
        elements.append(subject)

    for item in elements:
        chatgpt.train_assistent(item)

    print("System is now ready to rumbleeeeee!")
    while (user_input := input("Enter a question: ")) != "exit":
        print("OpenAI:", chatgpt.send_message_and_get_answer(user_input))


if __name__ == "__main__":
    chatgpt.setup()
    # print(chatgpt.send_message_and_get_answer("Ist SAP oder IBM besser?"))
    main()
