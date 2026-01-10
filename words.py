import re
import os
from collections import Counter

folder_path = "texts"
wrdcnt = Counter()

def szukaslow(path):
    with open(path, 'r', encoding="utf8") as file:
        listt=[]
        for line in file:
            listt.extend(_words_from_line(line))
    return listt
    
def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu unicode."
    words = re.split('[\W\d]+', line)
    for word in words:
        if word:
           wrdcnt[word] += 1
    return [w for w in words if w]

word_list = []
for filename in os.listdir("texts"):
    if filename.endswith('.txt'):
        file_path = os.path.join("texts", filename)
        words=szukaslow(file_path)
        word_list.append(words)

txtline = ''
count = 0

for count, key in enumerate(wrdcnt.most_common(), start=1):
    txtline += "{} {}\n".format(count, re.sub(r'[^a-zA-Z0-9ąęśżźćóńł_]', ' ', str(key)))

with open("frekwencyjna.csv", "w", encoding="utf8") as text_file:
    text_file.write(txtline)