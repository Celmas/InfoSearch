
import re
import pymorphy2


class BooleanParser:

    @staticmethod
    def parseString(query, inverted_index):
        result_set = set()
        operation = None
        analyzer = pymorphy2.MorphAnalyzer()

        first = True
        for word in re.split(" +(AND|OR) +", query):
            # word will be in ['foo', 'OR', 'bar', 'AND', 'NOT gazonk']

            inverted = False  # for "NOT word" operations

            if word in ['AND', 'OR']:
                operation = word
                continue

            if word.find('NOT ') == 0:
                if operation == 'OR':
                    # generally "OR NOT" operation does not make sense, but if it does in your case, you
                    # should update this if() accordingly
                    continue

                inverted = True
                # the word is inverted!
                realword = word[4:]
            else:
                realword = word

            if first:
                normal_form = analyzer.parse(realword)[0].normal_form
                if normal_form not in inverted_index:
                    print("There is no '{}' in inverted index".format(realword))
                    return set()
                result_set = inverted_index[normal_form]
                first = False

            if operation is not None:
                # now we need to match the key and the filenames it contains:
                normal_form = analyzer.parse(realword)[0].normal_form
                if normal_form not in inverted_index:
                    print("There is no '{}' in inverted index".format(realword))
                    return set()
                current_set = inverted_index[normal_form]

                if operation == 'AND':
                    if inverted is True:
                        result_set -= current_set
                    else:
                        result_set &= current_set
                elif operation == 'OR':
                    result_set |= current_set
            operation = None
        return result_set
