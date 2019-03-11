import os
import re


def tokenize(s):
    american_units = ['cup', 'tablespoon', 'teaspoon', 'pound', 'ounce', 'quart', 'pint']
    for unit in american_units:
        s = s.replace(unit + '/', unit + ' ')
        s = s.replace(unit + 's/', unit + 's ')
    return filter(None, re.split(r'([,()])?\s+', clumpFractions(s)))


def joinLine(columns):
    return "\t".join(columns)


def clumpFractions(s):
    return re.sub(r'(\d+)\s+(\d)/(\d)', r'\1$\2/\3', s)


def cleanUnicodeFractions(s):
    fractions = {u'\x215b': '1/8', u'\x215c': '3/8', u'\x215d': '5/8', u'\x215e': '7/8', u'\x2159': '1/6',
                 u'\x215a': '5/6', u'\x2155': '1/5', u'\x2156': '2/5', u'\x2157': '3/5', u'\x2158': '4/5',
                 u'\xbc': ' 1/4', u'\xbe': '3/4', u'\x2153': '1/3', u'\x2154': '2/3', u'\xbd': '1/2'}
    for f_unicode, f_ascii in fractions.items():
        s = s.replace(f_unicode, ' ' + f_ascii)
    return s


def unclump(s):
    return re.sub(r'\$', " ", s)


def getFeatures(token, index, tokens, length):
    return [
        ("I%s" % index),
        ("L%s" % lengthGroup(length)),
        ("Yes" if isCapitalized(token) else "No") + "CAP",
        ("Yes" if insideParenthesis(token, tokens) else "No") + "PAREN"
    ]


def singularize(word):
    units = {
        "cups": u"cup",
        "tablespoons": u"tablespoon",
        "teaspoons": u"teaspoon",
        "pounds": u"pound",
        "ounces": u"ounce",
        "cloves": u"clove",
        "sprigs": u"sprig",
        "pinches": u"pinch",
        "bunches": u"bunch",
        "slices": u"slice",
        "grams": u"gram",
        "heads": u"head",
        "quarts": u"quart",
        "stalks": u"stalk",
        "pints": u"pint",
        "pieces": u"piece",
        "sticks": u"stick",
        "dashes": u"dash",
        "fillets": u"fillet",
        "cans": u"can",
        "ears": u"ear",
        "packages": u"package",
        "strips": u"strip",
        "bulbs": u"bulb",
        "bottles": u"bottle"
    }

    if word in units.keys():
        return units[word]
    else:
        return word


def isCapitalized(token):
    return re.match(r'^[A-Z]', token) is not None


def lengthGroup(actualLength):
    for n in [4, 8, 12, 16, 20]:
        if actualLength < n:
            return str(n)
    return "X"


def insideParenthesis(token, tokens):
    if token in ['(', ')']:
        return True
    else:
        line = " ".join(tokens)
        return re.match(r'.*\(.*' + re.escape(token) + '.*\).*', line) is not None


def smartJoin(words):
    input = " ".join(words)
    input = input.replace(" , ", ", ")
    input = input.replace("( ", "(")
    input = input.replace(" )", ")")
    return input


def import_data(lines):
    data = [{}]
    display = [[]]
    prevTag = None
    for line in lines:
        if line in ('', '\n'):
            data.append({})
            display.append([])
            prevTag = None

        elif line[0] == "#":
            pass

        else:

            columns = re.split('\t', line.strip())
            token = columns[0].strip()

            token = unclump(token)

            tag, confidence = re.split(r'/', columns[-1], 1)
            tag = re.sub('^[BI]-', "", tag).lower()


            if prevTag != tag:
                display[-1].append((tag, [token]))
                prevTag = tag

            else:
                display[-1][-1][1].append(token)

            if tag not in data[-1]:
                data[-1][tag] = []

            if tag == "unit":
                token = singularize(token)

            data[-1][tag].append(token)

    output = [
        dict([(k, smartJoin(ingredient[k])) for k in ingredient])
        for ingredient in data
        if len(ingredient)
    ]

    return output


def export_data(lines):
    output = []
    for line in lines:
        line_clean = re.sub('<[^<]+?>', '', line)
        tokens = tokenize(line_clean)
        length = len(list(tokenize(line_clean)))

        for i, token in enumerate(list(tokens)):
            features = getFeatures(token, i + 1, tokens, length)
            output.append(joinLine([token] + features))
        output.append('')
    return '\n'.join(output)


def tag_ingredient_parts(text):
    model_file = os.path.join(os.path.dirname(__file__), "model_file")
    tmp_file = os.path.join(os.path.dirname(__file__), "tmp_file.txt")
    with open(tmp_file, 'w') as outfile:
        output = export_data([text])
        outfile.write(output)
    result = os.popen("crf_test -v 1 -m %s %s" % (model_file, tmp_file)).read()
    os.system("rm %s" % tmp_file)
    result = result.split("\n")
    return import_data(result)[0]