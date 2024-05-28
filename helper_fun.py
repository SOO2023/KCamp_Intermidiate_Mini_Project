from itertools import count

#a simple int id generator
def id_gen (n):
    for i in count(n):
        yield i + 1