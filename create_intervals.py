def create_intervals(set_of_ints):
    sorted_ints = sorted(set_of_ints)
    interval_list = []
    for i, el in enumerate(sorted_ints):
        if i == 0 or sorted_ints[i] != sorted_ints[i - 1] + 1:
            interval_list.append([el, el])
        else:
            interval_list[-1][1] = el
    return [tuple(interval) for interval in interval_list]
