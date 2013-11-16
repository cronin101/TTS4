from pydot import (Dot, Edge, Node)

import re
import lxml.etree as etree

class InterestingReader:
    def __init__(self, lines, emails, hub, auth):
        self.hub = hub
        self.auth = auth

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
            return self.email_lookup.get(email, email)

        highest_hub = max(self.hub.get(e, 0.0) for e in self.emails)
        highest_auth = max(self.auth.get(e, 0.0) for e in self.emails)

        def colour(email):
            def to_hex(score):
                return hex(int(score))[2:].zfill(2)

            auth_score = ((self.auth.get(email, 0.0) / highest_auth) * 250.0) + 5
            hub_score = ((self.hub.get(email, 0.0) / highest_hub) * 250.0) + 5

            return '#' + to_hex(255.0 - auth_score) + to_hex(100.00) + to_hex(255.0 - hub_score)

        graph = Dot(graph_type='digraph', simplify=True, suppress_disconnected=True)

        people = (Node(lookup(e), shape='record', style="filled", fillcolor=colour(e)) for e in self.emails)
        for node in people:
            graph.add_node(node)

        num_emails = []
        for sender in self.outgoing.keys():
            for receiver in self.outgoing[sender].keys():
                num_emails.append(len(self.outgoing[sender][receiver]))

        mean_emails = float(sum(num_emails)) / float(len(num_emails))

        links = []
        for sender in self.outgoing.keys():
            for receiver in self.outgoing[sender].keys():
                count = len(self.outgoing[sender][receiver])
                prop = float(count) / mean_emails
                if prop > 0.33:
                    links.append(Edge(lookup(sender), lookup(receiver), penwidth=((0.7 + (prop / 4.0))/ 2.0), weight=prop))
        for edge in links: graph.add_edge(edge)

        graph.write_png('./enron.png')
