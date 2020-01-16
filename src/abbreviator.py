from src import mapper, lister
from src import utils

ABB_PATH = "./maps/abbreviation.map"
PRENUM_ABB_PATH = "./maps/pre_number_abb.map"
POSTNUM_ABB_PATH = "./maps/post_number_abb.map"
FIRSTNAME_PATH = "./lists/firstnames.list"
SURNAME_PATH = "./lists/surnames.list"


def execute(sentence):
    sentence = basic(sentence)
    sentence = pre_number(sentence)
    sentence = post_number(sentence)
    sentence = full_name(sentence)
    return sentence


def basic(sentence):
    words = utils.tokenize(sentence)

    abb_map = mapper.load(ABB_PATH)

    for i in range(0, len(words)):
        word = utils.strip(words[i])
        if word in abb_map:
            words[i] = utils.replace(words[i], str(abb_map[word]))

    return " ".join(words)


def pre_number(sentence):
    words = utils.tokenize(sentence)

    abb_map = mapper.load(PRENUM_ABB_PATH, plural=True)

    for i in range(1, len(words)):
        word = utils.strip(words[i])
        if word in abb_map and utils.is_number(utils.strip(words[i-1])):
            words[i] = utils.replace(words[i], str(abb_map[word]))

    return " ".join(words)


def post_number(sentence):
    words = utils.tokenize(sentence)

    abb_map = mapper.load(POSTNUM_ABB_PATH, first_caps=True)

    for i in range(1, len(words)):
        word = utils.strip(words[i-1])
        if word in abb_map and utils.is_number(utils.strip(words[i])):
            words[i-1] = utils.replace(words[i-1], str(abb_map[word]))

    return " ".join(words)


def full_name(sentence):
    words = utils.tokenize(sentence)

    first_list = lister.load(FIRSTNAME_PATH)
    sur_list = lister.load(SURNAME_PATH)

    for i in range(1, len(words)):
        first = utils.strip(words[i-1])
        last = utils.strip(words[i])
        if last in sur_list and first in first_list:
            words[i-1] = utils.replace(words[i-1], str(first[:1] + "."))

    return " ".join(words)

