from query import Query


def is_float(text):
    return text.count(".") == 1 and text.replace(".", "").replace("E-", "").isnumeric()


def get_data(file_name):
    f = open(file_name)
    lines = [x.replace('"', '').replace('\n', '') for x in f.readlines()]
    criteria = lines[0].split(',')
    data = []
    for line in lines[1:]:
        values = line.split(',')
        entry = {}
        for c, v in zip(criteria, values):
            value = v
            if v.isdecimal():
                value = int(v)
            elif is_float(v):
                value = float(v)
            entry[c] = value
        data.append(entry)
    return data


if __name__ == "__main__":
    data = get_data("five-techs")
    query = Query(data).group_by("componentsQuantity").group_by("randomize")
    print(query.avg("res0"))
    print(query.avg("res1"))
    print(query.avg("res2"))