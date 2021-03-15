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


def get_normal_form(tokens, indx):
    analyzer = pymorphy2.MorphAnalyzer()
    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}
    normalized_words = dict()
    for token in tokens:
        parsed_word = analyzer.parse(token)
        if parsed_word[0].tag.POS in functors_pos: continue
        temp_set = set()
        for candidate in parsed_word:
            temp_set.add(candidate.normal_form)
        for normal_form in temp_set:
            normalized_words[normal_form] = {indx}
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


texts = dict()
for i in range(100):
    text = parse_text(i)
    text = sanitize_text(text)
    normalized_text = get_normal_form(text, i)
    for key, value in normalized_text.items():
        if key in texts:
            texts[key].update(value)
        else:
            texts[key] = value

with open("data/invertedIndex.txt", 'w', encoding='utf-8') as f:
    for key, value in texts.items():
        f.write(key + ' ' + str(sorted(value)) + '\n')

docs_indxs = set(range(0, 100))
operation_line = input('Напишите выражение вида: car AND apple | car OR apple | NOT car\n')
split_line = operation_line.split()
analyzer = pymorphy2.MorphAnalyzer()
if 'NOT' in operation_line:
    first = analyzer.parse(split_line[1])[0].normal_form
    if first not in texts:
        print('Слова ' + split_line[1] + ' нету')
    else:
        print(sorted(docs_indxs.difference(texts[first])))
else:
    first = analyzer.parse(split_line[0])[0].normal_form
    second = analyzer.parse(split_line[2])[0].normal_form
    if first not in texts:
        print('Слова ' + split_line[0] + ' нету')
    elif second not in texts:
        print('Слова ' + split_line[2] + ' нету')
    else:
        first_set = texts[first]
        second_set = texts[second]
        if 'AND' in operation_line:
            print(sorted(first_set.intersection(second_set)))
        elif 'OR' in operation_line:
            print(sorted(first_set.union(second_set)))
