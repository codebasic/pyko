"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""
import itertools
import abc
import reprlib
import re

from nltk.corpus import CorpusReader
from bs4 import BeautifulSoup


class TokenSeq(abc.ABC):
    def __init__(self, fileids, encoding):
        self.fileids = fileids
        self.encoding = encoding

    def __iter__(self):
        return itertools.chain(
                token for fid in self.fileids for token in self._get_token(fid) if token)

    def __len__(self):
        if not hasattr(self, 'length'):
            self.length = 0
            for _ in iter(self):
                self.length +=1
        return self.length

    def __getitem__(self, index):
        it = iter(self)
        if isinstance(index, slice):
            item_it = itertools.islice(it, index.start, index.stop, index.step)
            return [token for token in item_it]
        else:
            item_it = itertools.islice(it, index, index+1)
            return next(item_it)

    def __repr__(self):
        return reprlib.repr([token for token in itertools.islice(iter(self), 10)])

    @abc.abstractmethod
    def _get_token(self, fileid, tagged):
        """yield a token"""


class SejongCorpusReader(CorpusReader):
    """Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding='utf-16'):
        super().__init__(root, fileids, encoding)


    def words(self, fileids=None, tagged=False):
        """각 파일의 생성기 토큰을 하나의 생성기로 반환"""
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged)

    def sents(self, fileids=None, tagged=False):
        return SejongSentSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged)


class SejongWordSeq(TokenSeq):
    def __init__(self, fileids, encoding, tagged):
        super().__init__(fileids, encoding)
        self._tagged = tagged

    def _get_token(self, fileid):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all(re.compile('^s$|^p$'))

        for elt in sent_elt:
            if elt.find('note'):
                continue # skip <note>
            for line in elt.text.split('\n'):
                raw_token = line.split('\t')[-2:]
                if not raw_token[-1]:
                    continue

                token = raw_token[0]
                형태분석목록 = self._형태분석해독(raw_token)
                # 형태 분석 결과가 없는 경우 확인
                if not len(형태분석목록):
                    continue

                if self._tagged:
                    yield (token, 형태분석목록)
                else:
                    yield token

    def _형태분석해독(self, raw_token):
        형태분석목록 = []
        for tag in raw_token[-1].split('+'):
            형태소, 품사 = tuple(tag.split('/'))
            if not 형태소 or not 품사:
                continue
            형태분석목록.append((형태소, 품사))
        return tuple(형태분석목록)


class SejongSentSeq(TokenSeq):
    def __init__(self, fileids, encoding, tagged):
        super().__init__(fileids, encoding)
        self._tagged = tagged

    def _get_token(self, fileid):
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all('s')

        for elt in sent_elt:
            if elt.find('note'):
                continue # skip <note>
            sent = []
            for line in elt.text.split('\n'):
                raw_token = line.split('\t')[-2:]
                if not raw_token[-1]:
                    continue

                token = raw_token[0]
                형태분석목록 = tuple(tuple(tag.split('/')) for tag in raw_token[-1].split('+'))

                if self._tagged:
                    sent.extend(형태분석목록)
                else:
                    sent.append(token)
            yield sent
