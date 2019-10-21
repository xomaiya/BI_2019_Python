def checkio(first, second):
    words1 = first.split(',')
    words2 = second.split(',')
    intersec = set(words1) & set(words2)
    return ','.join(sorted(intersec))
