import json
import re
from collections import defaultdict

# Functions
def load_dataset(filename):
    with open(filename, 'r') as file:
        dataset = json.load(file)
        return dataset["data"]

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def build_ngram_dict(sentences, n=2):
    ngram_dict = defaultdict(int)
    for sentence in sentences:
        words = ['<start>'] + sentence.split() + ['<end>']
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            ngram_dict[ngram] += 1
    return ngram_dict

def predict_next_word(input_sentence, ngram_dict, n=2):
    input_sentence = preprocess_text(input_sentence)
    words = input_sentence.split()
    if len(words) < n - 1:
        return ""
    last_ngram = tuple(words[-(n-1):] + ['<end>'])
    predictions = {ngram[-1]: freq for ngram, freq in ngram_dict.items() if ngram[:-1] == tuple(last_ngram[:-1])}

    if predictions and '<end>' in predictions and len(predictions) > 1:
        del predictions['<end>']

    if not predictions:
        return "<end>"
    return max(predictions, key=predictions.get)

# Init
data = load_dataset('dataset.json')

# Input
input_sentence = input("Enter a word or phrase: ")

# Processor
preprocessed_data = [preprocess_text(sentence) for sentence in data]
ngram_dict = build_ngram_dict(preprocessed_data, n=2)
predicted_word = predict_next_word(input_sentence, ngram_dict, n=2)

# Output
print("Predicted word:", predicted_word)
