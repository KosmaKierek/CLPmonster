from flask import Flask, render_template
import os
import re
import operator

app = Flask(__name__)

tabWag = {
    'Sprawca': (['król', 'karol', 'charles', 'kardynał', 'biskup', 'rodzina', 'królewska', 'następca'], 0.25, 'rgb(249, 84, 84)'),
    'Zdarzenie': (['procesja', 'uroczystość', 'przyjęcie', 'msza', 'chrzest', 'celebracja'], 0.05, 'lightgreen'),
    'Obiekt': (['diamenty', 'kryształy', 'szata', 'insygnia', 'karoca'], 0.05, 'rgb(132, 116, 237)'),
    'Narzędzie': (['korona', 'berło', 'tron', 'kropielnica' ], 0.2, 'orange'),
    'Miejsce': (['pałac', 'zamek', 'buckingham', 'kościół', 'klasztor', 'Westminster', 'opactwo'], 0.25, 'yellow'),
    'Cel': (['koronacja', 'następstwo', 'objęcie'], 0.2, 'rgb(250, 93, 250)'),
}

def _words_from_line(line):
        "Zwraca listę słów dla linijki tekstu unicode."
        words = re.split('[\W\d]+', line)
        return [w for w in words if w]

class Text:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.categories = []
        self.weight = 0

class Corpus:
    def __init__(self):
        self.texts = []

    def fulltext(self):
        for filename in os.listdir('texts'):
            with open(f'texts/{filename}', 'r', encoding='utf-8') as file:
                text = file.read()
                self.texts.append(Text(text, filename))

    def make_categories(self):
        for sometext in self.texts:
            listt=[]
            listt.extend(_words_from_line(sometext.text))
            for word in listt:
                for key, value in tabWag.items():
                    if word.lower() in value[0]:
                        if key not in sometext.categories:
                            sometext.categories.append(key)
                            sometext.weight += value[1]
                        sometext.text = self.color_text(word, sometext.text, value[2])
    
    
    def color_text(self, word, text, color):
        end = "`!@#$%^&*()_+-=}{[]\|;:'<>?,./~ "
        for sign in end:
            replacement = f'<span style="background-color: {color}; font-style: italic; font-weight: bold;">{word}</span>{sign}'
            text = text.replace(word+sign, replacement)
        return text
    
    def run(self):
        self.fulltext()
        self.make_categories()
        self.texts = sorted(self.texts, key=operator.attrgetter('weight'), reverse=True)

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



# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port='12250')
