"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""

import os.path
from bs4 import BeautifulSoup

import pdb


class CorpusReader:
    def __init__(self, root, fileids):
        self.root = root
        self.resources = self.join(fileids)

    def join(self, fileids):
        resources = []
        for f in [fileids] if isinstance(fileids, str) else fileids:
            resources.append(os.path.join(self.root, f))
        return resources

    def get_fileids(self, fileids):
        if fileids:
            return self.join(fileids)
        else:
            return self.resources

    def fileids(self):
        return self.resources


class SejongCorpusReader(CorpusReader):
    """Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding=None):
        self.encoding = encoding
        CorpusReader.__init__(self, root, fileids)

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
