from collections import Counter

class GraphReader:
    def __init__(self, filename):

        with open(filename) as graph_file: lines = graph_file.readlines()

        self.raw = [l.strip().split() for l in lines]
        self.edges = Counter((out, inc) for (hsh, out, inc) in self.raw if out != inc)
