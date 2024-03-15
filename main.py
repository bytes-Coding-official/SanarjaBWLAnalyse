import Scraper
import Utility
import chatgpt

def main():
    for website in Utility.websites:
        mainsite = website.split("/")[2]
        if website not in Utility.url_tree:
            Utility.url_tree[mainsite] = Scraper.TreeNode(website)
        Scraper.analyse_websites(website)

    print(Utility.url_texts)

    elements = []
    for key, item in Utility.url_texts.items():
        subject = "von Website/Unternehmen " + key + " haben wir Informationen: " + item
        elements.append(subject)

    for item in elements:
        chatgpt.fill_assistant(item)
    # chatgpt.run_assistant()

    print("AI training completed system is now ready to rumbleeeeee!")
    while (user_input := input("Enter a question: ")) != "exit":
        print("OpenAI:", chatgpt.send_message_and_get_answer(user_input))


if __name__ == "__main__":
    chatgpt.setup()
    print(chatgpt.send_message_and_get_answer("Ist SAP oder IBM besser?"))
    # main()
