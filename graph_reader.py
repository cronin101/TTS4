from counter_backport import Counter

MAILING_LIST = 'pete.davis@enron.com'

class GraphReader:
    def __init__(self, filename):

        print("Reading file.")
        with open(filename) as graph_file: lines = graph_file.readlines()

        print("Building connections.")
        split = map(lambda l: l.strip().split(), lines)
        self.edges = Counter((out, inc) for (hsh, out, inc) in split
            if (not MAILING_LIST in (out, inc)) and out != inc)

if __name__ == "__main__":
    GraphReader('./graph.txt')
