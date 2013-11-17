import string
import operator
import enchant

from counter_backport import Counter



class EmailReader:
    def __init__(self, refs):
        with open('./legal_words.txt') as l: self.lwords = set(word.strip() for word in l.readlines())

        enxml = open('./enron.xml')

        docs = enxml.read().split('<DOCID> ')
        enxml.close()

        def get_ref(doc):
            doc_id = doc.split(' </DOCID>')[0]
            doc_ref = doc_id.split('/')[-1]
            return doc_ref

        def get_body(doc):
            front = doc.split('</DOC>')[0]
            back = front.split('</DOCID>')[1]
            return back

        self.kept = { get_ref(doc) : get_body(doc) for doc in docs if get_ref(doc) in refs }

    def process(self):
        tab = string.maketrans(
            string.ascii_uppercase + string.punctuation,
            string.ascii_lowercase + (' ' * len(string.punctuation))
        )

        self.kept = { k : Counter([word for word in string.translate(v,tab).split() if len(word) > 4 and word in self.lwords]) for (k, v) in self.kept.iteritems() }

        self.df = Counter([])
        for (k, v) in self.kept.iteritems():
            self.df.update(v)

        #print sorted(self.df.iteritems(), reverse=True, key=operator.itemgetter(1))

        return self

    def phoenix_rank(self, hshes):
        totals = Counter([])
        for counts in (v for (k, v) in self.kept.iteritems() if k in hshes):
            totals.update(counts)

        d = enchant.Dict()

        def is_word(w):
            return d.check(w)

        scores = { k : (v ** 2) / float(self.df[k]) for (k, v) in totals.iteritems() if is_word(k) }
        #scores = { k : v  for (k, v) in totals.iteritems() }
        return sum(scores.values()) / float(len(hshes))

if __name__ == "__main__":
    reader = EmailReader(set(['0000f70b82e8e7a34ea0703cff673aa4']))

    print reader.process().kept
    print reader.df

    print reader.highest_weighted(set(['0000f70b82e8e7a34ea0703cff673aa4']))
