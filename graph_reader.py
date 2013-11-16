from counter_backport import Counter

class GraphReader:
    def __init__(self, filename):

        with open(filename) as graph_file: lines = graph_file.readlines()

        split = (l.strip().split() for l in lines)
        self.edges = Counter((out, inc) for (hsh, out, inc) in split if out != inc)

if __name__ == "__main__":
    GraphReader('./graph.txt')
