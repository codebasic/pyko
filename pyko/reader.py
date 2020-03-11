"""
Copyright (C) 2017-2020 Codebasic
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
                self.length += 1
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
    def _get_token(self, fileid):
        """yield a token"""


class SejongCorpusReader(CorpusReader):
    """
    Corpus reader for 세종 말뭉치 (Sejong Corpus)
    """

    def __init__(self, root, fileids, encoding='utf-16'):
        super().__init__(root, fileids, encoding)

    def words(self, fileids=None, tagged=False, 형태분리=True):
        """
        말뭉치로부터 토큰 획득

        :param fileids: 말뭉치 파일 ID
        :type fileids: list[str] or None
        :return: 토큰 생성기
        :rtype: generator
        """
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged, 형태분리=형태분리)

    def sents(self, fileids=None, tagged=False, 형태분리=False):
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged, 형태분리=형태분리, sents=True)


class SejongWordSeq(TokenSeq):
    def __init__(self, fileids, encoding, tagged, 형태분리, sents=False):
        super().__init__(fileids, encoding)
        self._tagged = tagged
        self._형태분리 = 형태분리
        self._sents = sents

    def _get_token(self, fileid):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all(re.compile('^s$|^p$'))

        for elt in sent_elt:
            문장 = []
            if elt.find('note'):
                continue  # skip <note>
            for line in elt.text.split('\n'):
                raw_token = line.split('\t')[-2:]
                if not raw_token[-1]:
                    continue

                token = raw_token[0]
                # 어절이 없는 경우 확인
                if not token:
                    continue

                형태분석목록 = self._형태분석해독(raw_token)
                # 형태 분석 결과가 없는 경우 확인
                if not len(형태분석목록):
                    continue
                
                if not self._sents:
                    if self._tagged:
                        yield (token, 형태분석목록)
                    else:
                        yield token
                else: # 문장 단위인 경우
                    if self._tagged:
                        문장.append((token, 형태분석목록))
                    elif self._형태분리:
                        문장.extend(형태소 for 형태소, 품사 in 형태분석목록)
                    else:
                        문장.append(token)
            
            yield 문장

    def _형태분석해독(self, raw_token):
        형태분석목록 = []
        for tag in raw_token[-1].split('+'):
            try:
                형태소, _, 품사 = [원소 for 원소 in re.split('(/)', tag) if 원소]
            except ValueError:
                continue
            else:
                # 형태소 뒷번호 정리. 예: 세계__02 --> 세계
                형태소 = re.sub(r'__\d{1,}', '', 형태소)
                # 공백 제거
                형태소 = 형태소.strip()
                if not 형태소 or not 품사:
                    continue
                형태분석목록.append((형태소, 품사))
        return tuple(형태분석목록)