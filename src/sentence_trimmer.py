from src import sim_matrix, neural_network, utils, metrics

DEBUG = False

SIM_MATRIX_RATIO = 0.9
RN_RATIO = 0.1


def trim(data, ratio):
    initial = metrics.measure(data)
    final = initial * ratio/100

    score1 = sim_matrix.execute(data)
    score2 = neural_network.execute(data)
    utils.rescale(score1, SIM_MATRIX_RATIO)
    utils.rescale(score2, RN_RATIO)

    score = dict()
    line = []
    for i in range(len(score1)):
        score[i] = score1[i] + score2[i]
        line.append((i, score[i], len(data[i])))

    line.sort(key = lambda x: x[1], reverse = True)
    finals = []
    total = 0
    for i in line:
        if total + i[2] <= final:
            finals.append(i[0])
            total += i[2]

    finals.sort()

    finaldata = []
    for i in finals:
        finaldata.append(data[i])

    if DEBUG:
        print("SIM MATRIX: " + str(score1))
        print("RN: " + str(score2))
        print("Total: " + str(score))
    return finaldata
