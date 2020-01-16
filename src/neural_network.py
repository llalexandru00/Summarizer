from src import utils, lister
import numpy as np

AVOID_PATH = "./lists/avoid.list"
MAX_WORDS = 1e3
MAX_CHARS = 1e3
MAX_LENGTH = 1e4


def features(sentence):
    avoid = lister.load(AVOID_PATH)
    words = len(sentence.split(" "))
    length = len(sentence)
    clean = 0
    major = 0
    avoided = 0
    for i in sentence.split():
        word = utils.ultraStrip(i)
        if word in avoid:
            avoided += 1
            continue
        clean += len(word)
        if utils.strip(i)[0].isupper():
            major += 1
    quotes = 0
    dots = 0
    commas = 0
    spaces = 0
    for i in sentence:
        if i == "\"":
            quotes += 1
        if i == ".":
            dots += 1
        if i == ",":
            commas += 1
        if i == " ":
            spaces += 1

    return words, length, avoided, clean, major, quotes, dots, commas, spaces


def normalize(input):
    words = input[0] / MAX_WORDS
    length = input[1] / MAX_LENGTH
    avoided = input[2] / MAX_WORDS
    clean = input[3] / MAX_LENGTH
    major = input[4] / MAX_WORDS
    quotes = input[5] / MAX_CHARS
    dots = input[6] / MAX_CHARS
    commas = input[7] / MAX_CHARS
    spaces = input[8] / MAX_CHARS
    return words, length, avoided, clean, major, quotes, dots, commas, spaces


weights1 = []
weights2 = []


def isOut(txt):
    weights1 = np.load("./weights/weights1.npy")
    weights2 = np.load("./weights/weights2.npy")
    input = normalize(features(txt))
    backward(input)
    np.save("./weights/weights1.npy", weights1)
    np.save("./weights/weights2.npy", weights2)


def execute(data):
    global weights1
    global weights2
    inputs = []
    score = dict()

    weights1 = np.load("./weights/weights1.npy")
    weights2 = np.load("./weights/weights2.npy")

    for i in data:
        inputs.append(normalize(features(i)))

    for i in range(len(inputs)):
        score[i] = answer(inputs[i])[0]

    return score


# Full RN algorithm
RANDOM_SEED = 101
LEARNING_RATE = 0.01


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def forward(inputs):
    global weights1
    global weights2
    output_from_layer1 = sigmoid(np.dot(inputs, weights1))
    output_from_layer2 = sigmoid(np.dot(output_from_layer1, weights2))
    return output_from_layer1, output_from_layer2


def backward(training_set_inputs, training_set_outputs, output_from_layer_1, output_from_layer_2):
    global weights1
    global weights2

    layer2_error = training_set_outputs - output_from_layer_2
    layer2_delta = layer2_error * LEARNING_RATE

    layer1_error = layer2_delta.dot(weights2.T)
    layer1_delta = layer1_error * LEARNING_RATE

    layer1_adjustment = training_set_inputs.T.dot(layer1_delta)
    layer2_adjustment = output_from_layer_1.T.dot(layer2_delta)

    weights1 += layer1_adjustment
    weights2 += layer2_adjustment


def answer(probe):
    hidden_state, score = forward(np.array(probe))
    return score


np.random.seed(RANDOM_SEED)