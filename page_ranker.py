import operator

class PageRanker:
    def __init__(self, counted_edges, lbda=0.8):
        self.lbda = lbda

        senders = set(out for out, inc in counted_edges.keys())
        receivers = set (inc for out, inc in counted_edges.keys())
        self.unique_emails = senders | receivers

        self.outlinks = {}
        for (out, inc), weight in counted_edges.iteritems():
            self.outlinks[out] = self.outlinks.get(out, []) + ([inc] * weight)

        self.sinks = self.unique_emails - senders

        self.page_rank = {}
        initial_rank = 1.0 / len(self.unique_emails)
        self.page_rank = { email : initial_rank for email in self.unique_emails }

    def iterate(self, n):
        for it in xrange(n):
            lm = self.lbda

            leaked_pr = lm * sum(self.page_rank[email] for email in self.sinks)
            random_walk_pr = 1.0 - lm

            initial_pr = (leaked_pr + random_walk_pr) / len(self.unique_emails)

            next_page_rank = { email : initial_pr for email in self.unique_emails }

            for sender, recipients in self.outlinks.iteritems():
                received_pr = lm * (self.page_rank[sender] / len(recipients))
                for recipient in recipients:
                    next_page_rank[recipient] += received_pr

            self.page_rank = next_page_rank
        return self

    def highest(self, n):
        return sorted(self.page_rank.iteritems(), key=operator.itemgetter(1), reverse=True)[:n]
