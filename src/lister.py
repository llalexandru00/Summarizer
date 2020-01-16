def load(path, first_caps = False):
    file = open(path, "r", encoding='utf-8', errors='ignore')
    lines = file.readlines()
    l = list()
    for line in lines:
        tokens = line.split()
        if len(tokens) != 1:
            continue
        l.append(tokens[0].strip())
    if first_caps:
        l = capitalize(l)
    return set(l)


def capitalize(l):
    ans = []
    for i in l:
        ans.append(i)
        ans.append(i.capitalize())
    return ans
