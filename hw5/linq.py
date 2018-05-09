from myitertools import chain, groupby, islice


class Linq(object):
    def __init__(self, iterable):
        self._iterable = iterable

    def select(self, func):
        return Linq(map(func, self._iterable))

    def flatten(self):
        return Linq(chain(*self._iterable))

    def where(self, func):
        return Linq(filter(func, self._iterable))

    def take(self, n):
        return Linq(islice(self._iterable, n))

    def group_by(self, func):
        return Linq(groupby(self._iterable, func))

    def order_by(self, func):
        return Linq(sorted(self._iterable, key=func))

    def to_list(self):
        return list(self._iterable)

    def __iter__(self):
        return self._iterable
