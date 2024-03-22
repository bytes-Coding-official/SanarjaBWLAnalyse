import time

from openai import OpenAI

data_cache = dict()
client = None
thread = None
thread_id = None
assistant = None
DEBUG = True


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
            # print loaded assistent with assistent description
            print("loaded assistent,", assistant.description)
        except Exception:
            assistant = client.beta.assistants.create(
                name="ERP-Instructor",
                description="ERP Instructor for AI and ERP Systems",
                instructions="Du bist nun ein QA Tool das nutzern auf basis von ihnen vorher bereitgestelltem Wissens antworten in einer kurzen und bündigen Form wiedergibt.",
                model="gpt-4-turbo-preview",
            )
            with open('api.key', 'a') as file:
                file.write(assistant.id + "\n")
            if DEBUG:
                print("new assistant created")

    with open('api.key', 'r') as file:
        try:
            thread_id = file.readlines()[2].strip()
            thread = client.beta.threads.retrieve(thread_id=thread_id)
            # print loaded thread with thread messages
            print("loaded thread,", thread.messages)
        except Exception:
            with open('api.key', 'a') as file:
                thread = client.beta.threads.create()
                thread_id = thread.id
                file.write(thread.id + "\n")
            if DEBUG:
                print("new thread created")
    # Variable zum Verfolgen des Run-Status
    if DEBUG:
        print("Checking the status of the latest run...")

    # Den neuesten Run abrufen, davon ausgehend, dass der letzte Run in der Liste der neueste ist
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    latest_run = runs.data[0] if runs.data else None

    # Warten, bis der neueste Run abgeschlossen ist
    while latest_run and latest_run.status == "in_progress":
        time.sleep(3)  # Vermeiden Sie zu häufige Anfragen
        # Run-Status aktualisieren, um den aktuellen Zustand zu überprüfen
        latest_run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=latest_run.id)
        if DEBUG:
            print("Latest run is still in progress...")

    if DEBUG:
        print("Latest run completed.")

        # Optional: Weitere Logik hier, falls nötig
    if DEBUG:
        print("Alle Runs sind abgeschlossen. Context: Setup")
    # Den Assistenten auf den aktualisierten Thread anwenden, um eine Antwort zu erhalten

    with open("messages.txt", "r") as file:
        for line in file.readlines():
            if ":!:" in line:
                key, value = line.split(":!:")
                data_cache[key] = value
        else:
            if DEBUG:
                print("cache loaded from file")
    if DEBUG:
        print("setup completed")


def train_assistent(messages):
    for message in messages:
        fill_assistant(message)
    run_assistant()
    if DEBUG:
        print("Training done...")


def fill_assistant(message):
    # Nur den neuesten Run für den Thread abrufen, da nur dieser relevant für den aktuellen Kontext ist
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    latest_run = runs.data[0] if runs.data else None

    if latest_run and latest_run.status == "in_progress":
        if DEBUG:
            print("Waiting for the latest run to complete before adding a new message...")

        while latest_run.status == "in_progress":
            time.sleep(5)  # Vermeiden Sie zu häufige Anfragen
            # Run-Status aktualisieren, um den aktuellen Zustand zu überprüfen
            latest_run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=latest_run.id)
            if DEBUG:
                print("Run in progress...")

    if DEBUG:
        print("Ready to add a new message. All previous runs are completed.")

    if DEBUG:
        print("Adding message:", message)

    # Nachricht zum Thread hinzufügen
    created_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    if DEBUG:
        print("Message filled and added to the thread:", created_message.content[0].text.value)


def run_assistant():
    texts = client.beta.threads.messages.list(thread_id=thread_id)
    if DEBUG:
        for message in texts.data:
            print("message:", message.content[0].text.value)

    # Erstellen und Starten eines Runs
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id
    )
    print("Assistant started")

    # Warten, bis der Run abgeschlossen ist
    while run.status == "in_progress":
        time.sleep(5)  # Vermeiden Sie zu häufige Anfragen
        # Run-Status aktualisieren, um den aktuellen Zustand zu überprüfen
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print("Run in progress...")

    if DEBUG:
        print("Assistant completed")

    return run


# sleep for 5 seconds

def send_message_and_get_answer(message):
    if message in data_cache:
        if DEBUG:
            print("Found message in cache, loading answer...")
        return data_cache[message]
    else:
        fill_assistant(message)
        run = run_assistant()
        answer = get_latest_message_from_run(run, message)
        return answer


def write_cache_to_file(message, answer):
    if message not in data_cache:
        data_cache[message] = answer
    with open("messages.txt", "w") as file:
        for key, value in data_cache.items():
            file.write(key + ":!:" + value + "\n")
    if DEBUG:
        print("cache written to file")


def get_latest_message_from_run(run, message=""):
    # Warten Sie, bis der Run abgeschlossen ist, bevor Sie die Nachrichten abrufen
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    while run.status != "completed":
        time.sleep(3)  # Kurze Pause, um zu verhindern, dass die API zu häufig aufgerufen wird
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    # Nachrichten im Thread auflisten, nachdem der Run abgeschlossen ist
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    # Die letzte Nachricht im Thread sollte die Antwort des Assistenten sein
    if messages.data:
        # Filtern Sie die Nachrichten, um nur die Antworten des Assistenten zu erhalten
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        if assistant_messages:
            answer = assistant_messages[-1].content[0].text.value
            if DEBUG:
                print("Last message from assistant:", answer)
            write_cache_to_file(message, answer)
            return answer
    else:
        if DEBUG:
            print("No messages found in the thread or no answer generated")
        return None
