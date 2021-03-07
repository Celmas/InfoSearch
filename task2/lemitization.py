import os
import nltk
import pymorphy2
import re
from lxml import etree
from typing import Final

RE_D: Final = re.compile('\d')


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
    normalized_words = dict()
    for token in tokens:
        parsed_word = analyzer.parse(token)
        if parsed_word[0].tag.POS in functors_pos: continue
        temp_set = set()
        for candidate in parsed_word:
            temp_set.add(candidate.normal_form)
        normalized_words[token] = temp_set
    return normalized_words


def contains_numeric(string):
    return RE_D.search(string)


def append_to_file(filename, content):
    os.makedirs("data", exist_ok=True)
    with open("data/" + filename, 'a', encoding='utf-8') as f:
        f.write(str.join('\n', content))


def sanitize_text(text_to_process):
    text_to_process = text_to_process.replace('.', ' ')  # in case of рублей.Большинство
    text_to_process = text_to_process.replace('|', ' ')  # in case of Gizmochina|SparrowsNewsWestern
    tokens = nltk.word_tokenize(text_to_process)
    puncto = [',', '.', ':', '?', '«', '»', '-', '(', ')', '!', '\'', '—', ';', '”', '...', '\"', '``', '@', '\'\'',
              '%', '--', '[', ']', '=', '+', '*', '\\', '$', '~', '&']
    return [token for token in tokens if token not in puncto and not contains_numeric(token)]


texts = list()
for i in range(100):
    text = parse_text(i)
    text = sanitize_text(text)
    append_to_file('Words.txt', text)
    normalized_text = get_normal_form(text)
    texts.append(normalized_text)

with open("data/Lems.txt", 'a', encoding='utf-8') as f:
    for text in texts:
        for key, value in text.items():
            f.write(key + ' ' + str.join(' ', value) + '\n')
