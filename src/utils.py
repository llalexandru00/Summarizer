def tokenize(sentence):
    return sentence.split()


def strip(word):
    return word.strip(",!?.()[];:{}\"'")


def ultraStrip(word):
    word = strip(word)
    if len(word) >= 2 and word[-2] == "'":
        word = word[:-2]
    return word.lower()


def replace(old, changed):
    core = strip(old)
    return old.replace(core, changed)


def is_number(word):
    try:
        int(word)
        return True
    except ValueError:
        return False


def rescale(score, ratio):
    maxim = max(score.values())
    scale = ratio/maxim
    for i in score.keys():
        score[i] *= scale
