import os
import nltk
import pymorphy2
from collections import Counter
import math
import re
from lxml import etree
from typing import Final

RE_D: Final = re.compile('\d')


def compute_tfidf(corpus):
    def compute_tf(text):
        tf_text = Counter(text)
        for i in tf_text:
            tf_text[i] = tf_text[i] / float(len(text))
        return tf_text

    def compute_idf(word, corpus):
        return math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))

    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            computed_idf = compute_idf(word, corpus)
            tf_idf_dictionary[word] = [computed_idf, computed_tf[word] * computed_idf]
        documents_list.append(tf_idf_dictionary)
    return documents_list


def parse_text(filename):
    with open("../task1/data/" + str(filename) + ".html", "r", encoding="UTF-8") as html:
        htmlparser = etree.HTMLParser()
        tree = etree.parse(html, htmlparser)
        texts_from_html = tree.xpath('//p//text()')
        concatenated_text = str.join('', texts_from_html)
        return concatenated_text


def get_normal_form(tokens):
    analyzer = pymorphy2.MorphAnalyzer()
    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}
    normalized_words = []
    for token in tokens:
        parsed_word = analyzer.parse(token)
        if parsed_word[0].tag.POS in functors_pos: continue
        for candidate in parsed_word:
            normalized_words.append(candidate.normal_form)
    return normalized_words


def contains_numeric(string):
    return RE_D.search(string)


def sanitize_text(text_to_process):
    text_to_process = text_to_process.replace('.', ' ')  # in case of рублей.Большинство
    text_to_process = text_to_process.replace('|', ' ')  # in case of Gizmochina|SparrowsNewsWestern
    tokens = nltk.word_tokenize(text_to_process)
    puncto = [',', '.', ':', '?', '«', '»', '-', '(', ')', '!', '\'', '—', ';', '”', '...', '\"', '``', '@', '\'\'',
              '%', '--', '[', ']', '=', '+', '*', '\\', '$', '~', '&']
    return [token for token in tokens if token not in puncto and not contains_numeric(token)]


texts = []
for i in range(100):
    text_parsed = parse_text(i)
    text_parsed = sanitize_text(text_parsed)
    normalized_text = get_normal_form(text_parsed)
    texts.append(normalized_text)

tfidf = compute_tfidf(texts)
#TF-IDF for every word
os.makedirs("data", exist_ok=True)
g = open("data/out.txt", "w", encoding="UTF-8")
for dictionary in tfidf:
    print(dictionary, file=g)
