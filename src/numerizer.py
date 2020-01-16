from src import mapper
from src import utils

NUM_PATH = "./maps/number.map"


# converts words to numbers
def execute(sentence):
    words = utils.tokenize(sentence)
    parsed = []
    last_ok = -1
    num_map = mapper.load(NUM_PATH)
    for i in range(0, len(words)):
        word = words[i]
        changed = utils.strip(word)
        if changed in num_map and last_ok < i:
            number = 0
            buffer = 0
            last_ok = i
            for j in range(i, len(words)):
                actual = words[j]
                actual = utils.strip(actual)
                if actual not in num_map:
                    break

                if num_map[actual] == '1000000':
                    if buffer == 0:
                        break
                    else:
                        number += 1000000 * buffer
                        buffer = 0
                elif num_map[actual] == '1000':
                    if buffer == 0:
                        break
                    else:
                        number += 1000 * buffer
                        buffer = 0
                elif num_map[actual] == '100':
                    buffer = buffer * 100
                else:
                    buffer += int(num_map[actual])
                last_ok = j
                if actual != words[j]:
                    break

            number += buffer
            parsed.append(utils.replace(words[last_ok], str(number)))
        else:
            if last_ok < i:
                parsed.append(utils.replace(word, changed))
    return " ".join(parsed)
