from graph_reader import GraphReader
from page_ranker  import PageRanker

ranker = PageRanker(GraphReader('./graph.txt').edges)

for x in xrange(10): ranker.iterate()

with open('./pr.txt', 'w') as p_ranks:
    p_ranks.write('\n'.join(' '.join(["%.8f" % score, str(person)]) for (person, score) in ranker.highest(10)) + '\n')
