def group_equal(els):
    group_list = []
    for i, el in enumerate(els):
        if i == 0 or els[i] != els[i - 1]:
            group_list.append([el])
        else:
            group_list[-1].append(el)
    return group_list
