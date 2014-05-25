from itertools import groupby


def gr(l, cr):
    result = {}
    for k, v in groupby(l, lambda x: x[cr]):
        grouped = result.get(k, [])
        for x in v:
            grouped.append(x)
        result[k] = grouped
    return {k: Query(v) for k, v in result.items()}


class Query(object):
    def __init__(self, data):
        self.data = data

    def eq(self, criteria, value):
        return Query([x for x in self.data if x[criteria] == value])

    def filter(self, criteria, f):
        return Query([x for x in self.data if f(x[criteria])])

    def avg(self, criteria):
        mapped = [x[criteria] for x in self.data]
        return sum(mapped) / len(mapped)

    def true(self, criteria):
        return self.filter(criteria, lambda x: x.lower() == "true")

    def group_by(self, criteria):
        return GroupByQuery(gr(self.data, criteria))

    def get(self):
        return self.data


class GroupByQuery(Query):
    def __init__(self, data):
        self.data = data

    def delegate(self, fun):
        return GroupByQuery({k: fun(v) for k, v in self.data.items()})

    def eq(self, criteria, value):
        return self.delegate(lambda q: q.eq(criteria, value))

    def filter(self, criteria, f):
        return self.delegate(lambda q: q.filter(criteria, f))

    def avg(self, criteria):
        return {k: v.avg(criteria) for k, v in self.data.items()}

    def group_by(self, criteria):
        return self.delegate(lambda q: q.group_by(criteria))

    def true(self, criteria):
        return self.delegate(lambda q: q.true(criteria))

    def get(self):
        return {k: v.get() for k, v in self.data.items()}


