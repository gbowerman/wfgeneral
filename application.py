from flask import Flask, render_template, request
import sys

HOST = '0.0.0.0'
PORT = 8081
WORDFILE = 'words.txt'

app = Flask(__name__)
wordlist = []

def load_words():
    '''load words of matching length from a file into a list of lists by word length'''
    wordlist = [[] for i in range(30)]
    try:
        with open(WORDFILE) as wf:
            for word in wf:
                wordlen = len(word) - 1  # remove linefeed from word
                wordlist[wordlen].append(word[:-1])
    except FileNotFoundError:
        sys.exit('Error: cannot open file ' + WORDFILE)
    return wordlist


def word_match(partial_word, word, wordlen):
    '''return true if partial word matches word'''
    for x in range(wordlen):
        if partial_word[x] == '?':
            continue
        if partial_word[x] != word[x]:
            return False
    return True


def wordfind(partial_word):
    '''finds matching words in a list - '?' is wild'''
    wordlen = len(partial_word)
    resultlist = []
    for word in wordlist[wordlen]:
        if word_match(partial_word, word, wordlen):
            #print(word)
            resultlist.append(word)
    return resultlist

def anagfind(anagram):
    '''finds an anagram by comparing two sorted strings'''
    wordlen = len(anagram)
    srtdarr = sorted(anagram)
    resultlist = []
    for word in wordlist[wordlen]:
        if srtdarr == sorted(word):
            #print(word)
            resultlist.append(word)
    return resultlist

def initapp():
    global wordlist
    wordlist = load_words()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods = ['POST', 'GET'])
def findword():
    word = request.form['partial']
    resultlist = wordfind(word)
    return render_template('results.html', result = resultlist)

@app.route('/anagram', methods = ['POST', 'GET'])
def anagram():
    word = request.form['anagram']
    resultlist = anagfind(word)
    return render_template('results.html', result = resultlist)


if __name__ == '__main__':
    initapp()
    app.run(host=HOST, port=PORT)