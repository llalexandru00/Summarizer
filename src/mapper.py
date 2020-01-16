SAFE_MAP = "./maps/safe.map"


def load(path, plural = False, first_caps = False):
    file = open(path, "r", encoding='utf-8', errors='ignore')
    lines = file.readlines()
    d = dict()
    for line in lines:
        tokens = line.split()
        if len(tokens) < 3:
            continue
        _from = tokens[0]
        _to = tokens[2]
        d[_from] = _to
    if plural:
        d = pluralize(d)
    if first_caps:
        d = capitalize(d)
    return d


def pluralize(d):
    ans = dict()
    for i in d.keys():
        ans[i] = d[i]
        ans[i+'s'] = d[i]
    return ans


def capitalize(d):
    ans = dict()
    for i in d.keys():
        ans[i] = d[i]
        ans[i.capitalize()] = d[i].capitalize()
    return ans


def safe(word):
    map = load(SAFE_MAP)
    if word in map.keys():
        return map[word]
    return word