from graph_reader import GraphReader
from page_ranker  import PageRanker

ranker = PageRanker(GraphReader('./graph.txt').edges).iterate(9)

with open('./pr.txt', 'w') as p_ranks:
    p_ranks.write('\n'.join(' '.join(["%.8f" % s, e]) for (e, s) in ranker.highest(10)) + '\n')
