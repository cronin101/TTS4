from graph_reader import GraphReader
from page_ranker  import PageRanker
from hub_auth_ranker import HubAuthRanker

page_ranker = PageRanker(GraphReader('./graph.txt').edges).iterate(10)

hub_auth_ranker = HubAuthRanker(GraphReader('./graph.txt').edges).iterate(10)

def dump(ostream, ranks):
    ostream.write('\n'.join(' '.join(["%.8f" % s, e]) for (e, s) in ranks) + '\n')

with open('./pr.txt', 'w') as p_r: dump(p_r, page_ranker.highest(10))

with open('./hub.txt', 'w') as hub_r: dump(hub_r, hub_auth_ranker.highest_hubs(10))

with open('./auth.txt', 'w') as auth_r: dump(auth_r, hub_auth_ranker.highest_auths(10))
