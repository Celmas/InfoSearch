import streamlit as st
import pandas as pd

from BooleanParser import BooleanParser


def create_boolean_string(_search):
    _search = _search.split(" ")
    _search = [s.strip() for s in _search]
    return str.join(" AND ", _search)


def parse_inverted_index(filename):
    _inverted_index = dict()
    with open("data/" + str(filename) + ".txt", "r", encoding="UTF-8") as f:
        for line in f:
            word = line[:line.find(' ')]
            array = line[line.find(' '):]
            array = array[2:-2].split(',')
            array = [s.strip() for s in array]
            _inverted_index[word] = set(array)
    return _inverted_index


def parse_sites(filename):
    _sites = dict()
    with open("data/" + str(filename) + ".txt", "r", encoding="UTF-8") as f:
        for line in f:
            sites_array = line.split(' - ')
            _sites[sites_array[0]] = sites_array[1]
    return _sites


def get_list_urls(_set, _sites):
    _urls = list()
    for item in _set:
        _urls.append(_sites[item])
    return _urls


st.write("#Search")
st.write("Введите строку для поиска")
search = st.text_input("Gogole")

# Init
inverted_index = parse_inverted_index("invertedindex")
sites = parse_sites("index")

if st.button("Искать"):
    boolean_search_line = create_boolean_string(search)
    result = BooleanParser.parseString(boolean_search_line, inverted_index)
    urls_list = get_list_urls(result, sites)
    urls_pd = pd.DataFrame(urls_list, columns=["Сайты"])
    if not urls_list:
        st.write("Ничего не найдено")
    else:
        st.table(urls_pd)