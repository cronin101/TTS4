from graph_reader import GraphReader

import itertools

class PageRanker:
    def __init__(self, counted_edges):

        senders = set(out for out, inc in counted_edges.keys())
        receivers = set (inc for out, inc in counted_edges.keys())
        self.unique_emails = senders | receivers

        self.outlinks = {}
        for (out, inc), weight in counted_edges.iteritems():
            self.outlinks[out] = self.outlinks.get(out, []) + ([inc] * weight)

        self.sinks = self.unique_emails - senders

        self.page_rank = {}
        initial_rank = 1.0 / len(self.unique_emails)
        self.page_rank = dict((email, initial_rank) for email in self.unique_emails)

    def iterate(self):
        lbda = 0.8

        leaked_pr = lbda * sum(self.page_rank[email] for email in self.sinks)
        random_walk_pr = 1.0 - lbda

        initial_pr = (leaked_pr + random_walk_pr) / len(self.unique_emails)

        next_page_rank = dict((email, initial_pr) for email in self.unique_emails)

        for sender, recipients in self.outlinks.iteritems():
            received_pr = lbda * (self.page_rank[sender] / len(recipients))
            for recipient in recipients:
                next_page_rank[recipient] += received_pr

        print "PR total: " + str(sum(next_page_rank.values()))

        self.page_rank = next_page_rank


ranker = PageRanker(GraphReader('./graph.txt').edges)

for x in xrange(10): ranker.iterate()

print ranker.page_rank['jeff.dasovich@enron.com']
