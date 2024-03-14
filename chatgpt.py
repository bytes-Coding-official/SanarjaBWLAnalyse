import time

from openai import OpenAI

with open('api.key', 'r') as file:
    api_key = file.readline().strip()
# Definiere eine Session-ID
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)

with open('api.key ', 'r') as file:
    try:
        assistant_id = file.readlines()[1].strip()
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    except Exception:
        assistant = client.beta.assistants.create(
            name="ERP-Instructor",
            description="ERP Instructor for AI and ERP Systems",
            instructions="Your a consultant related to ERP Programs and AI so you tell the customer if System X or Y uses Ai in der ERP system and how or which ERP system uses Ai based on their question. You are strict in your answers and very clear. So no fillers like: it depends on ... that the user",
            model="gpt-4-turbo-preview",
        )

        with open('api.key', 'a') as file:
            file.write(assistant.id + "\n")

with open('api.key', 'r') as file:
    try:
        thread_id = file.readlines()[2].strip()
        thread = client.beta.threads.retrieve(thread_id=thread_id)
    except Exception:
        with open('api.key', 'a') as file:
            thread = client.beta.threads.create()
            file.write(thread.id + "\n")

messages = []


def fill_assistant(message):
    content = {"role": "user", "content": message}
    messages.append(content)


def run_assistant():
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while run.status != "completed":
        time.sleep(1)
    return run


# sleep for 5 seconds


# Den Assistenten auf den aktualisierten Thread anwenden, um eine Antwort zu erhalten
new_run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)


def get_latest_message_from_run():
    # Abrufen der Nachrichten im Thread
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    # Überprüfen, ob Nachrichten vorhanden sind
    if messages.data:
        # Ausgeben der Nachrichten (optional)
        for message in messages.data:
            print(message.content[0].text.value)

        # Rückgabe der letzten Nachricht
        return messages.data[-1].content[0].text.value
    else:
        # Keine Nachrichten gefunden
        return None

# 
# def send_message(prompt="") -> str:
#     response = client.chat.completions.create(
#         model="gpt-4-0125-preview",
#         messages=[
#             {"role": "system",
#              "content": "Du bist ein Assistent der berät in bezug auf ERP Systeme und KI du bekommst Informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
#             {"role": "user",
#              "content": "Antworte möglichst Knapp und direkt und erfinde keine Informationen berufe dich auf das Wissen das du bekommen hast und fantasiere nicht gib mir konkrete antworten" + prompt},
#         ],
#         n=1,
#         seed=42,
#         max_tokens=4096,
#         temperature=0,
#     )
#     print("response", response)
#     print(response.choices[0].message['content'])
#     return response.choices[0].message['content']
# 
# 
# def train(prompt="") -> str:
#     response = client.chat.completions.create(
#         model="gpt-4-0125-preview",
#         messages=[
#             {"role": "system",
#              "content": "Du bist ein Assistent der berät in bezug auf ERP Systeme und KI du bekommst Informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
#             {"role": "user",
#              "content": "Antworte möglichst Knapp und direkt und erfinde keine Informationen berufe dich auf das Wissen das du bekommen hast und fantasiere nicht gib mir konkrete antworten" + prompt},
#         ],
#         temperature=0
#     )
#     print(response.choices[0].message['content'])
#     return response.choices[0].message['content']
