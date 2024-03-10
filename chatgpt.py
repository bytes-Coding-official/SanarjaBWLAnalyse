from openai import OpenAI

with open('api.key', 'r') as file:
    api_key = file.readline().strip()
# Definiere eine Session-ID
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)

session_id = 'meine-einzigartige-session-id-sanarja-abbas2024-03'


def send_message(prompt="") -> str:
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": "Du bist ein Assistent der berät in bezug auf ERP Systeme und KI du bekommst Informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
            {"role": "user",
             "content": "Antworte möglichst Knapp und direkt und erfinde keine Informationen berufe dich auf das Wissen das du bekommen hast und fantasiere nicht gib mir konkrete antworten" + prompt},
        ],
        n=1,
        seed=42,
        max_tokens=5000,
        temperature=0,
    )
    print("response", response)
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']


def train(prompt="") -> str:
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": "Du bist ein Assistent der berät in bezug auf ERP Systeme und KI du bekommst Informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
            {"role": "user",
             "content": "Antworte möglichst Knapp und direkt und erfinde keine Informationen berufe dich auf das Wissen das du bekommen hast und fantasiere nicht gib mir konkrete antworten" + prompt},
        ],
        temperature=0
    )
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']
