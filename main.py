from graph_reader import GraphReader
from page_ranker  import PageRanker
from hits_ranker import HITSRanker
from interesting_reader import InterestingReader

N_ITER = 10
N_RESULTS = 10

input_graph = GraphReader('./graph.txt')
edgeset = input_graph.edges

page_ranker = PageRanker(edgeset).iterate(N_ITER)

hits_ranker = HITSRanker(edgeset).iterate(N_ITER)

def dump(ostream, ranks):
    ostream.write('\n'.join(' '.join(["%.8f" % s, e]) for (e, s) in ranks) + '\n')

with open('./pr.txt', 'w') as p_r: dump(p_r, page_ranker.highest(N_RESULTS))

with open('./hub.txt', 'w') as hub_r: dump(hub_r, hits_ranker.highest_hubs(N_RESULTS))

with open('./auth.txt', 'w') as auth_r: dump(auth_r, hits_ranker.highest_auths(N_RESULTS))

print "pr " + ("%.8f" % page_ranker.page_rank['jeff.dasovich@enron.com'])
print "hub " + ("%.8f" % hits_ranker.hub['jeff.dasovich@enron.com'])
print "auth " + ("%.8f" % hits_ranker.auth['jeff.dasovich@enron.com'])

interesting_people = set(e for (e, s) in page_ranker.highest(40))

# Remove the mailing list bot
try:
    interesting_people.remove('pete.davis@enron.com')
except: KeyError

InterestingReader(input_graph.raw, interesting_people, hits_ranker.hub, hits_ranker.auth).make_graph()
