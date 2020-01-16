import numpy as np

NR_FEATURES = 9
HIDDEN_LAYER_SIZE = 3
OUTPUT_SIZE = 1


def randomize(weights, number_of_neurons, number_of_inputs_per_neuron):
    w = np.random.random((number_of_inputs_per_neuron, number_of_neurons))
    for i in w:
        weights.append(i)


weights1 = []
weights2 = []
randomize(weights1, HIDDEN_LAYER_SIZE, NR_FEATURES)
randomize(weights2, OUTPUT_SIZE, HIDDEN_LAYER_SIZE)
weights1 = np.array(weights1)
weights2 = np.array(weights2)
np.save("./weights/weights1.npy", weights1)
np.save("./weights/weights2.npy", weights2)