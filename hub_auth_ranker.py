import operator
import math

class HubAuthRanker:
    def __init__(self, counted_edges):
        self.senders = set(out for out, inc in counted_edges.keys())
        self.receivers = set(inc for out, inc in counted_edges.keys())
        self.unique_emails = self.senders | self.receivers

        self.outlinks, self.inlinks = {}, {}

        for (out, inc), weight in counted_edges.iteritems():
            self.outlinks[out] = self.outlinks.get(out, []) + ([inc] * weight)
            self.inlinks[inc]  = self.inlinks.get(inc, []) + ([out] * weight)

        initial_score = 1.0/math.sqrt(len(self.unique_emails))
        self.hub = { email : initial_score for email in self.unique_emails }
        self.auth = { email : initial_score for email in self.unique_emails }

    def iterate(self, n):
        for it in xrange(n):
            self.hub = { email : sum(self.auth[target] for target in self.outlinks[email]) for email in self.senders }
            hub_norm_factor = 1.0 / math.sqrt(sum(value ** 2 for value in self.hub.values()))
            self.hub = { e : s * hub_norm_factor for e, s in self.hub.iteritems() }

            self.auth = { email : sum(self.hub[sender] for sender in self.inlinks[email]) for email in self.receivers }
            auth_norm_factor = 1.0 / math.sqrt(sum(value ** 2 for value in self.auth.values()))
            self.auth = { e : s * auth_norm_factor for e, s in self.auth.iteritems() }
        return self

    def highest_hubs(self, n):
        return sorted(self.hub.iteritems(), key=operator.itemgetter(1), reverse=True)[:n]

    def highest_auths(self, n):
        return sorted(self.auth.iteritems(), key=operator.itemgetter(1), reverse=True)[:n]
