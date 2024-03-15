import time

from openai import OpenAI

data_cache = dict()
messages = []
client = None
thread = None
thread_id = None
assistant = None
debug = True


def setup():
    global client
    global thread
    global thread_id
    global assistant
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
                instructions="I am an AI that can answer questions about ERP systems. Antworte auf Fragen zu ERP-Systemen. und Antworte auch immer auf deutsch",
                model="gpt-4-turbo-preview",
            )

            with open('api.key', 'a') as file:
                file.write(assistant.id + "\n")
            if debug:
                print("new assistant created")

    with open('api.key', 'r') as file:
        try:
            thread_id = file.readlines()[2].strip()
            thread = client.beta.threads.retrieve(thread_id=thread_id)
        except Exception:
            with open('api.key', 'a') as file:
                thread = client.beta.threads.create()
                thread_id = thread.id
                file.write(thread.id + "\n")
            if debug:
                print("new thread created")
    # Variable zum Verfolgen des Run-Status
    run_in_progress = True
    while run_in_progress:
        run_in_progress = False
        # Alle Runs für den Thread abrufen
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        # Über alle Runs iterieren
        for run in runs.data:
            if run.status == "in_progress":
                if debug:
                    print("Run in progress...")
                time.sleep(3)  # Kurze Pause, um zu verhindern, dass die API zu häufig aufgerufen wird
                run_in_progress = True

        # Optional: Weitere Logik hier, falls nötig
    if debug:
        print("Alle Runs sind abgeschlossen.")
    # Den Assistenten auf den aktualisierten Thread anwenden, um eine Antwort zu erhalten
    client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    if debug:
        print("setup completed")


def fill_assistant(message):
    # Variable zum Verfolgen des Run-Status
    run_in_progress = True

    while run_in_progress:
        run_in_progress = False  # Beendet die while-Schleife beim nächsten Durchlauf
        # Alle Runs für den Thread abrufen
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        # Über alle Runs iterieren
        for run in runs.data:
            if run.status == "in_progress":
                if debug:
                    print("Run in progress...")
                time.sleep(5)  # Kurze Pause, um zu verhindern, dass die API zu häufig aufgerufen wird
                run_in_progress = True
        # Optional: Weitere Logik hier, falls nötig
    if debug:
        print("Alle Runs sind abgeschlossen.")

    messages.append(message)
    # check if a run is active
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    if debug:
        print("Message filled")


def run_assistant():
    # print all messages in the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    if debug:
        for message in messages.data:
            print("message:", message.content[0].text.value)
        print("assistant started")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while run.status == "in_progress":
        time.sleep(5)
    if debug:
        print("assistant completed")
    return run


# sleep for 5 seconds

def send_message_and_get_answer(message):
    if message in data_cache:
        return data_cache[message]
    else:
        fill_assistant(message)
        # run_assistant()
        message = get_latest_message_from_run()
        return message


def write_cache_to_file():
    with open("messages.txt", "w") as file:
        for key, value in data_cache.items():
            file.write(key + ":!:" + value + "\n")
    if debug:
        print("cache written to file")


def get_latest_message_from_run():
    # Abrufen der Nachrichten im Thread
    text = client.beta.threads.messages.list(thread_id=thread_id)
    # Überprüfen, ob Nachrichten vorhanden sind
    if text.data and debug:
        # Ausgeben der Nachrichten (optional)
        # Rückgabe der letzten Nachricht
        last_send = messages[-1]
        last_answer = text.data[-1].content[0].text.value
        last_answer = last_answer.replace("\n", " ")
        data_cache[last_send] = last_answer
        write_cache_to_file()
        return last_answer
    else:
        # Keine Nachrichten gefunden
        return None
