from graph_reader import GraphReader
from page_ranker  import PageRanker
from hub_auth_ranker import HubAuthRanker

N_ITER = 10
N_RESULTS = 10

edgeset = GraphReader('./graph.txt').edges

page_ranker = PageRanker(edgeset).iterate(N_ITER)

hub_auth_ranker = HubAuthRanker(edgeset).iterate(N_ITER)

def dump(ostream, ranks):
    ostream.write('\n'.join(' '.join(["%.8f" % s, e]) for (e, s) in ranks) + '\n')

with open('./pr.txt', 'w') as p_r: dump(p_r, page_ranker.highest(N_RESULTS))

with open('./hub.txt', 'w') as hub_r: dump(hub_r, hub_auth_ranker.highest_hubs(N_RESULTS))

with open('./auth.txt', 'w') as auth_r: dump(auth_r, hub_auth_ranker.highest_auths(N_RESULTS))
