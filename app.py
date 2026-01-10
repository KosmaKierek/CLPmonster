from flask import Flask, render_template
import os
import re

app = Flask(__name__)

tabWag = {
    'Sprawca': (['król', 'Charles', 'kardynał', 'biskup', 'rodzina', 'królewska', 'następca'], 0.25, 'rgb(249, 84, 84)'),
    'Zdarzenie': (['procesja', 'uroczystość', 'przyjęcie', 'msza', 'chrzest', 'celebracja'], 0.05, 'lightgreen'),
    'Obiekt': (['diamenty', 'kryształy', 'szata', 'insygnia', 'karoca'], 0.05, 'lightblue'),
    'Narzędzie': (['korona', 'berło', 'tron', 'kropielnica' ], 0.2, 'orange'),
    'Miejsce': (['zamek', 'Buckingham', 'kościół', 'klasztor', 'Westminster', 'opactwo'], 0.25, 'yellow'),
    'Cel': (['koronacja', 'następstwo', 'objęcie'], 0.2, 'rgb(250, 93, 250)'),
}
znaki = "`!@#$%^&*()_+-=}{[]\|;:'<>?,./~ "


class Text:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.categories = []
        self.weight = 0

class Corpus:
    def __init__(self):
        self.texts = []
        self.total_categories = 0
        self.total_weight = 0

    def fulltext(self):
        for filename in os.listdir('texts'):
            with open(f'texts/{filename}', 'r', encoding='utf-8') as file:
                text = file.read()
                self.texts.append(Text(text, filename))

#jesli nie usunie najpierw znakow to w liscie beda
#pod clp do zmiany
    def make_categories(self):
        for text_object in self.texts:
            clear_text = text_object.text
            for znak in znaki:
                clear_text = clear_text.replace(znak, " ")
            for word in clear_text.split(" "):
                for key, value in tabWag.items():
                    word_forms = [word.lower()]
  
                    for word_form in word_forms:
                        if word_form in value[0] or word in value[0]:
                            if key not in text_object.categories:
                                text_object.categories.append(key)
                                text_object.weight += value[1]
                            text_object.text = self.color_text(word, text_object.text, value[2])

    def color_text(self, word, text, color):
        for znak in znaki:
            replacement = f'<span style="background-color: {color}; font-style: italic; font-weight: bold;">{word}</span>{znak}'
            text = text.replace(word+znak, replacement)
        return text
    
    def run(self):
        self.fulltext()
        self.make_categories()

txtCorp = Corpus()
txtCorp.run()

@app.route('/')
def main():
    return render_template('index.html', texts=txtCorp.texts)

@app.route("/categories")
def category():
    return render_template('categories.html', tabWag=tabWag)

@app.route("/frequency")
def words():
    word_list = []
    with open('frekwencyjna.csv', 'r', encoding="utf8") as file:
        text = file.readlines()
        for line in text:
            row = line.split()
            word_list.append(row)
    return render_template('wordfreq.html', slowa=word_list)

if __name__ == '__main__':
    app.run()

