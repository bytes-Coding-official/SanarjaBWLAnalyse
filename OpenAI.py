import openai

openai.api_key = ""
# Definiere eine Session-ID
session_id = 'meine-einzigartige-session-id'


def send_message(prompt="") -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein Assistent der berät in bezug auf erp systeme und KI du bekommst informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        session_id=session_id
    )
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']


def train(prompt="") -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein Assistent der berät in bezug auf erp systeme und KI du bekommst informationen gegeben und sollst dann ratschläge geben auf basis des gegebenen wissens. Du sollst knapp und simpel die frage direkt beantworten ohne viel auszuschweifen. Du musst nur die frage direkt beantworten und nicht mehr sagen. der kontext sind ERP systeme und ob jene KI nutzen und in wie weit diese KI nutzen."},
            {"role": "system", "content": prompt},
        ],
        temperature=0,
        session_id=session_id
    )
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']
