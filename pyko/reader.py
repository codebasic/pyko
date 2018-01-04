"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""
import itertools

from nltk.corpus.reader.api import CorpusReader
from bs4 import BeautifulSoup

class SejongCorpusReader(CorpusReader):
    """Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding='utf-16'):
        super().__init__(root, fileids, encoding)


    def words(self, fileids=None, tagged=True):
        """각 파일의 생성기 토큰을 하나의 생성기로 반환"""
        return itertools.chain(token for fileid in self.abspaths(fileids) for token in self._get_words(fileid, tagged))
            
    def _get_words(self, fileid, tagged=True):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self._encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all('s')

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
                    yield (token, tagged_tokens)
                else:
                    yield token
