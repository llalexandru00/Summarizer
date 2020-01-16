def read_data(path):
    input_file = open(path, "r")
    lines = input_file.readlines()
    sentences = []
    for line in lines:
        chunks = line.split(". ")
        for chunk in chunks:
            if chunk.strip(".\n") != '':
                sentences.append(chunk.strip(".\n"))
    return sentences


def read_ratio(path):
    input_file = open(path, "r")
    lines = input_file.readlines()
    return int(lines[0])
