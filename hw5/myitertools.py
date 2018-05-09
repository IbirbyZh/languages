def chain(*args):
    for iterable in args:
        for element in iterable:
            yield element


def islice(iterable, count):
    for _, element in zip(range(count), iterable):
        yield element


def groupby(iterable, key_func):
    l = sorted(map(lambda x: (key_func(x), x), iterable), key=lambda x: x[0])
    if not l:
        return
    first_index = 0
    current_key = l[0][0]
    for i, (key, _) in enumerate(l):
        if key != current_key:
            yield (current_key, (x[1] for x in l[first_index:i]))
            first_index = i
            current_key = key
    yield (current_key, (x[1] for x in l[first_index:]))
