import gensim
import os


class DocSimilarity(object):
    def __init__(self, in_dir):
        """Read data"""
        self.lyric_list = []
        self.fnames = []
        for fname in os.listdir(in_dir):
            self.fnames.append(fname)
            filename = os.path.join(in_dir, fname)
            lyric = open(filename, encoding='utf-8', errors='ignore').read()
            self.lyric_list.append(list(lyric))

        self.corpus_pr()

    def corpus_pr(self):
        """gensim tf_idf computation"""
        dictionary = gensim.corpora.Dictionary(self.lyric_list)
        corpus = [dictionary.doc2bow(lyric) for lyric in self.lyric_list]
        tf_idf = gensim.models.TfidfModel(corpus)

        self.dictionary = dictionary
        self.corpus = corpus
        self.tf_idf = tf_idf

    def remove_sim(self, out_dir, max_similarity=0.3):
        """remove similar lyric and save one"""
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        c_corpus = [self.corpus[0]]
        open(os.path.join(out_dir, self.fnames[0]),
            'w', encoding='utf-8').write(''.join(self.lyric_list[0]))

        for i in range(1, len(self.corpus)):
            sims = gensim.similarities.Similarity('',
                self.tf_idf[c_corpus], num_features=len(self.dictionary))
            if sims[self.corpus[i]].max() < max_similarity:
                c_corpus.append(self.corpus[i])
                open(os.path.join(out_dir, self.fnames[i]),
                    'w', encoding='utf-8').write(''.join(self.lyric_list[i]))


if __name__ == '__main__':
    singer = '邓丽君'
    docsim = DocSimilarity(singer)
    docsim.remove_sim(singer + '_clean', max_similarity=0.3)
