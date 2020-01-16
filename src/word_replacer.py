from src import numerizer
from src import abbreviator


def numerize(sentence):
    return numerizer.execute(sentence)


def abbreviate(sentence):
    return abbreviator.execute(sentence)
