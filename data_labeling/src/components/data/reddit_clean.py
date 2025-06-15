import csv
import os
import re

def split_entry(text, max_len=1500):
    # Split at newlines first
    lines = text.split('\n')
    chunks = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # If line is short, just add it
        if len(line) <= max_len:
            chunks.append(line)
        else:
            # Split long line at sentence boundaries
            sentences = re.split(r'(?<=[.!?]) +', line)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) + 1 <= max_len:
                    current += (" " if current else "") + sent
                else:
                    if current:
                        chunks.append(current.strip())
                    current = sent
            if current:
                chunks.append(current.strip())
    return chunks

input_csv = "/Users/mayamarkus-malone/Documents/VADMAP/data/reddit_posts.csv"
output_csv = "/Users/mayamarkus-malone/Documents/VADMAP/data/reddit_posts_clean.csv"

with open(input_csv, "r", encoding="utf-8") as infile, \
     open(output_csv, "w", encoding="utf-8", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    header = next(reader)
    writer.writerow(header)
    for row in reader:
        post = row[0]
        vad = row[1] if len(row) > 1 else ""
        chunks = split_entry(post)
        for chunk in chunks:
            writer.writerow([chunk, vad])