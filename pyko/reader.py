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

    def sents(self, fileids=None, strip_space=True, stem=False):
        fileids = self.get_fileids(fileids)

        sents = []
        for fid in fileids:
            soup = BeautifulSoup(open(fid, encoding=self.encoding), 'lxml')
            body = soup.find('text')
            sent_tags = body.find_all('s')
            sents += [t.text for t in sent_tags]

        return sents
