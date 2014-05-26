#!/usr/bin/env python
import sys
from query import Query

def is_float(text):
    return text.count(".") == 1


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
            done = False
            if is_float(v):
              try:
                value = float(v)
                done = True
              except ValueError:
                pass

            if not done:
              try:
                value = int(v)
                done = True
              except ValueError:
                pass

            entry[c] = value
        data.append(entry)
    f.close()
    return data


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
      print "Usage: ", sys.argv[0], " [input_file]"
      sys.exit(-1)
    data = get_data(args[0])
    query = Query(data).group_by("numDomains").group_by("isRandom")
    print query.get()
    for x in query.get():
      print x
      print ""
      print ""
      print ""
    print(query.avg("item 0 adopters"))
    print(query.avg("item 1 adopters"))
    print(query.avg("misfits"))

