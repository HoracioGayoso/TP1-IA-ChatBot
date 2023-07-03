import json
import random

import numpy as np
import spacy
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
with open('intents.json') as file:
    intents = json.load(file)

nlp = spacy.load('en_core_web_sm')
ignore_tokens = ['?', '!', '.', ',']

documents = []
classes = []
words = []

# Process the intents
for intent in intents['intents']:
    tag = intent['tag']
    patterns = intent['patterns']
    responses = intent['responses']

    # Tokenize the patterns
    tokenized_patterns = []
    for pattern in patterns:
        tokens = []
        for token in nlp(pattern):
            if token.text not in ignore_tokens:
                tokens.append(token.lemma_)
        tokenized_patterns.append(tokens)

    # Add the patterns and responses to the training data
    for tokens in tokenized_patterns:
        documents.append((tokens, tag))
    classes.append(tag)

    # Extend the words list with tokens from each pattern
    words.extend([token for pattern in tokenized_patterns for token in pattern])


# Sort the list of words
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
print(words)


training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [nlp(word.lower())[0].lemma_ for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
train_x = np.array([data[0] for data in training])
train_y = np.array([data[1] for data in training])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x),
                np.array(train_y), epochs=500, batch_size=5, verbose=1)

model.save('chatbot_model.h5', hist)
print("Done")