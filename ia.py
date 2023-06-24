import spacy
import random
from spacy.util import minibatch, compounding

# Datos de entrenamiento
train_data = [
    ("Hola", {"cats": {"SALUDO": 1, "PREGUNTA": 0, "DESCONOCIDO": 0}}),
    ("Cómo estás?", {"cats": {"SALUDO": 0, "PREGUNTA": 1, "DESCONOCIDO": 0}}),
    ("Qué hora es?", {"cats": {"SALUDO": 0, "PREGUNTA": 1, "DESCONOCIDO": 0}}),
    ("Dónde está la biblioteca?", {"cats": {"SALUDO": 0, "PREGUNTA": 1, "DESCONOCIDO": 0}})
]

# Configurar el pipeline de spaCy
nlp = spacy.blank("es")
textcat = nlp.create_pipe("textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})
nlp.add_pipe(textcat)

# Añadir las etiquetas de intención al clasificador
textcat.add_label("SALUDO")
textcat.add_label("PREGUNTA")
textcat.add_label("DESCONOCIDO")

# Entrenar el modelo
optimizer = nlp.begin_training()
for epoch in range(10):
    random.shuffle(train_data)
    losses = {}
    batches = minibatch(train_data, size=8)
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer, losses=losses)
    print("Epoch:", epoch, "Loss:", losses)

# Ejemplo de interacción con el chatbot
while True:
    user_input = input("Ingresa tu mensaje: ")
    if user_input.lower() == "salir":
        break
    doc = nlp(user_input)
    intent = doc.cats
    predicted_label = max(intent, key=intent.get)
    print("Intención:", predicted_label)
