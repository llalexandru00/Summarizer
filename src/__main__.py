import sys
from src import processing, word_replacer, metrics, sentence_trimmer, neural_network

DEBUG = False


def apply(data, f, split = False, ratio = None):
    initial = metrics.measure(data)
    if split:
        changed = list(map(f, data))
    else:
        changed = f(data, ratio)
    final = metrics.measure(changed)
    if DEBUG:
        print(str(f) + " " + str(100 - final*100/initial) + "%")
    return changed


# Processing stage

if sys.argv[1] == "backit":
    txt = sys.argv[2]
    neural_network.isOut(txt)
    exit(0)


# This is the part where the text is split in atoms (sentences)
data = processing.read_data(sys.argv[1])
ratio = processing.read_ratio(sys.argv[2])

initial = metrics.measure(data)

# Layers
data = apply(data, sentence_trimmer.trim, ratio = ratio)

data = apply(data, word_replacer.numerize, split=True)
data = apply(data, word_replacer.abbreviate, split=True)

for i in data:
    print(i, end = ".\n")

final = metrics.measure(data)

if DEBUG:
    print("Initial: " + str(initial))
    print("Final: " + str(final))
    print("Ratio: " + str(final*100/initial))
