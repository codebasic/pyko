"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""

import os.path
from nltk.corpus.reader.api import CorpusReader
from bs4 import BeautifulSoup

class SejongCorpusReader(CorpusReader):
    """Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding='utf8'):
        super().__init__(root, fileids, encoding)

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
        fileids = self.get_fileids(fileids)

        words = []
        if not tagged:
            raise NotImplemented

        for fid in fileids:
            soup = BeautifulSoup(open(fid, encoding=self.encoding), 'lxml')
            body = soup.find('text')
            sent_tags = body.find_all('s')

            for tag in sent_tags:
                for line in tag.text.split('\n')[1:]:
                    word = line.split('\t')[1]
                    if word:
                        words.append(word)

        return words