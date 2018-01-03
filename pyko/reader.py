"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""

from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.util import concat
from bs4 import BeautifulSoup

class SejongCorpusReader(CorpusReader):
    """Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding='utf8', lazy=False):
        super().__init__(root, fileids, encoding)
        self._lazy = lazy

    def sents(self, fileids=None, tagged=False):
        fileids = self.get_fileids(fileids)

        sents = []
        for fid in fileids:
            soup = BeautifulSoup(open(fid, encoding=self.encoding), 'lxml')
            body = soup.find('text')
            sent_tags = body.find_all('s')
            if not tagged:
                sents += [t.text for t in sent_tags]
            else:
                for tag in sent_tags:
                    words = []
                    for line in tag.text.split('\n')[1:]:
                        word = line.split('\t')[1]
                        if word:
                            words.append(word)
                    sent = ' '.join(words)
                    if sent:
                        sents.append(sent)

        return sents

    def words(self, fileids=None, tagged=True):
#        f = SejongWordView if self._lazy else self._words
        f = self._words
        return concat([f(fileid, tagged) for fileid in self.abspaths(fileids)])
            
    def _words(self, fileid, tagged=True, encoding='utf-16'):
        soup = BeautifulSoup(open(fileid, encoding=self._encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all('s')

        words = []
        for elt in sent_elt:
            if elt.find('note'):
                continue # skip <note>
            for line in elt.text.split('\n'):
                raw_token = line.split('\t')[-2:]
                if not raw_token[-1]:
                    continue
                
                token = raw_token[0]
                tagged_tokens = tuple(tuple(tag.split('/')) for tag in raw_token[-1].split('+'))

                if tagged:
                    words.append((token, tagged_tokens))
                else:
                    words.append(token)

        return words
    