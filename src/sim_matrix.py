from src import utils, lister
import networkx as nx
from nltk.cluster.util import cosine_distance
import numpy as np

AVOID_PATH = "./lists/avoid.list"


def get_similarity(s1, s2, avoid):
    s1 = list(map(utils.ultraStrip, s1.split(" ")))
    s2 = list(map(utils.ultraStrip, s2.split(" ")))

    full = set()
    for word in s1:
        full.add(word)
    for word in s2:
        full.add(word)

    full = list(full)
    d = dict()
    for i in range(len(full)):
        d[full[i]] = i

    v1 = [0 for _ in range(len(full))]
    v2 = [0 for _ in range(len(full))]
    for word in s1:
        if word in avoid:
            continue
        v1[d[word]] += 1

    for word in s2:
        if word in avoid:
            continue
        v2[d[word]] += 1

    return 1 - cosine_distance(v1, v2)


def execute(data):
    avoid = lister.load(AVOID_PATH)
    matrix = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            matrix[i][j] = get_similarity(data[i], data[j], avoid)

    graph = nx.from_numpy_array(matrix)
    scores = nx.pagerank(graph)
    return scores