from transformers import pipeline
import json

def chunkify(text, chunk_size=100):
    return text

def preProcessEntry(journal):
    # end result: {date: {chunk: []}}
    #enters chunked
    processed = {}
    for date, chunks in journal.items():
        processed[date] = {}
        for chunk in chunks:
            processed[date][chunk] = []  # or [0, 0, 0] or any initial list
    return processed

def processEntry(map):
    classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
    for date in map:
        for chunk in map[date]:
            prediction = classifier(chunk)
            map[date][chunk] = prediction  # Replace the empty list with the prediction, or append if you want to keep a list
    return map

def caller(journal):
    map = preProcessEntry(journal)
    popMap = processEntry(map)
    return popMap

if __name__ == "__main__":
    journal = []
    with open('journals/firsTest.json', 'r') as file:
        journal = json.load(file)

    # this journal is pre chunked, will have to be chunked before
    map = caller(journal)
    print(map)