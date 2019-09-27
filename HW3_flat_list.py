def flat_list(ls):
    return sum([flat_list(el) if type(el) is list else [el] for el in ls], [])
