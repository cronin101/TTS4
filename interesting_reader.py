from pydot import (Dot, Edge, Node)
from email_reader import EmailReader
import math

import string
import re
import lxml.etree as etree

class InterestingReader:
    def __init__(self, lines, emails, hub, auth, pr):
        self.hub = { e : hub.get(e, 0.0) for e in emails }
        self.auth = { e : auth.get(e, 0.0) for e in emails }
        self.pr = { e : pr[e] for e in emails }

        valid = ((h, o, i) for (h, o, i) in lines
                if ((o != i) and o in emails and i in emails))

        interesting_emails = set()
        self.outgoing = {}
        for (hsh, out, inc) in valid:
            self.outgoing[out] = self.outgoing.get(out, {})
            self.outgoing[out][inc] = self.outgoing[out].get(inc, [])
            self.outgoing[out][inc].append(hsh)
            interesting_emails.add(hsh)

        self.emails = emails
        print "There are this many interesting emails: " +str(len(list(interesting_emails)))
        self.e_reader = EmailReader(interesting_emails).process()

        self.email_lookup = {}
        with open('./roles.txt') as roles: role_lines = roles.readlines()

        for line in role_lines:
            email, identity = line.strip().split('\t')[:2]
            identity_parts = [part for part in re.split(r'\s{2,}', identity) if not part in ['N/A', 'Employee']]
            identity = '\n'.join(identity_parts)
            if identity != 'xxx':
                self.email_lookup[email + '@enron.com'] = identity

    def make_graph(self):

        def lookup(email):
            return self.email_lookup.get(email, email) + '\n H=' + ("%.0e" % self.hub.get(email, 0.0)) + ', A=' + ("%.0e" % self.auth.get(email, 0.0))

        highest_hub = max(self.hub.get(e, 0.0) for e in self.emails)
        highest_auth = max(self.auth.get(e, 0.0) for e in self.emails)
        highest_hubauth = max(highest_hub, highest_auth)

        def mean(s): return sum(s) * 1.0 / len(s)
        def std_dev(mean_v, s): return math.sqrt(mean(map(lambda x: (x - mean_v)**2, s)))

        mean_hub = mean(self.hub.values())
        mean_auth = mean(self.auth.values())

        def colour(email):
            def to_hex(score):
                return hex(int(score))[2:].zfill(2)

            auth_score = ((self.auth.get(email, 0.0) / highest_auth) * 255.0)
            hub_score = ((self.hub.get(email, 0.0) / highest_hub) * 255.0)

            return '#' + to_hex(255.0 - auth_score) + '00' + to_hex(255.0 - hub_score)

        graph = Dot(graph_type='digraph', simplify=True, suppress_disconnected=True)

        mean_pr = mean(self.pr.values())

        people = (Node(lookup(e), shape='record', color=colour(e), fontsize=5.0 + (5.0 * (self.pr[e] / mean_pr))) for e in self.emails)
        for node in people:
            graph.add_node(node)

        num_emails = []
        for sender in self.outgoing.keys():
            for receiver in self.outgoing[sender].keys():
                num_emails.append(len(self.outgoing[sender][receiver]))

        mean_emails = mean(num_emails)
        email_std_dev = std_dev(mean_emails, num_emails)

        p_ranks = []
        for sender in self.outgoing.keys():
            for receiver in self.outgoing[sender].keys():
                p_ranks.append(self.e_reader.phoenix_rank(self.outgoing[sender][receiver] + self.outgoing.get(receiver, {}).get(sender, [])))

        mean_p_rank = mean(p_ranks)
        p_rank_std_dev = std_dev(mean_p_rank, p_ranks)

        links = []
        for sender in self.outgoing.keys():
            for receiver in self.outgoing[sender].keys():
                count = len(self.outgoing[sender][receiver])
                prop = float(count) / mean_emails
                if count >= mean_emails + (email_std_dev / 4):
                    #content = ' '.join(self.e_reader.highest_weighted(set(self.outgoing[sender][receiver])))
                    phoenix_rank =  self.e_reader.phoenix_rank(self.outgoing[sender][receiver] + self.outgoing.get(receiver, {}).get(sender, []))
                    if phoenix_rank >= (p_rank_std_dev / 3) + mean_p_rank:
                        color = "#ff0000"
                    else:
                        color = "#000000"

                    links.append(Edge(lookup(sender), lookup(receiver), color=color, penwidth=((0.7 + (prop / 4.0))/ 2.0), weight=prop))
        for edge in links: graph.add_edge(edge)

        graph.write_png('./enron.png')
        graph.write('enron.dot', format='raw', prog='dot')
