# from collections import Counter


def chekio(ls):
    # counter = Counter(ls)
    # return [el for el in ls if counter[el] > 1]
    return [el for el in ls if ls.count(el) > 1]
