from transformers import AutoTokenizer
from transformers import Trainer, TrainingArguments

# Modell und Tokenizer laden

max_length = 1024


def split_into_passages(text, max_length=max_length):
    words = text.split()
    passages = []
    current_passage = []

    for word in words:
        current_passage.append(word)
        if len(current_passage) >= max_length:
            passages.append(" ".join(current_passage))
            current_passage = []

    # Fügen Sie den verbleibenden Teil hinzu, wenn vorhanden
    if current_passage:
        passages.append(" ".join(current_passage))

    return passages


# Angenommen, `books` ist eine Liste von Texten der Bücher

def train_ai(items):
    passages = [passage for item in items for passage in split_into_passages(item)]

    model_name = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    model = AutoTokenizer.from_pretrained(model_name)

    # Tokenisieren Sie die Passagen
    # Tokenisieren Sie die Passagen
    tokenized_inputs = model(passages, padding=True, truncation=True, max_length=max_length, return_tensors="pt")

    # Modell laden

    # Training Arguments definieren
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=2,  # Diese Größe kann je nach verfügbarer GPU-Speicher angepasst werden
    )

    # Trainer initialisieren
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_inputs,
        # eval_dataset könnte ebenfalls definiert werden, falls Sie einen Evaluierungsdatensatz haben
    )

    # Training starten
    trainer.train()
