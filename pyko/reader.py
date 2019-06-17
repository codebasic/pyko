"""
Copyright (C) 2017-2018 Codebasic

Author: Lee Seongjoo <seongjoo@codebasic.io>
"""
import itertools
import abc
import reprlib
import re
import os.path

from nltk.corpus import CorpusReader
from bs4 import BeautifulSoup
import pandas as pd


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

    def words(self, fileids=None, tagged=False, 어절=False):
        """
        말뭉치로부터 토큰 획득

        :param fileids: 말뭉치 파일 ID
        :type fileids: list[str] or None
        :return: 토큰 생성기
        :rtype: generator
        """
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged, 어절=어절)

    def sents(self, fileids=None, **options):
        return SejongSentSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, **options)

    def tagged_sents(self, fileids=None):
        return self.sents(fileids, tagged=True)

    def token_sents(self, fileids=None):
        return self.sents(fileids, token=True)

    @property
    def tagset(self):
        return SejongCorpusReader.get_tagset()

    @staticmethod
    def get_tagset():
        tagset_file = os.path.join(os.path.dirname(__file__), 'data/sejong_tagset.json')
        tagset = pd.read_json(tagset_file, orient='index')
        return tagset


class SejongWordSeq(TokenSeq):
    def __init__(self, fileids, encoding, tagged, 어절):
        super().__init__(fileids, encoding)
        self._tagged = tagged
        self._어절 = 어절

    def _get_token(self, fileid):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
        # 구어
        sent_elt = body.find_all('s')

        for elt in sent_elt:
            if elt.find('note'):
                continue  # skip <note>
            for line in elt.text.split('\n'):
                raw_token = line.split('\t')[-2:]
                if not raw_token[-1]:
                    continue

                token = raw_token[0]
                tagged_tokens = tuple(tuple(tag.split('/'))
                                      for tag in raw_token[-1].split('+'))

                if self._tagged:
                    yield (token, tagged_tokens)
                else:
                    for word, tag in tagged_tokens:
                        yield word

        # 문어
        for 문단요소 in body.find_all('p'):
            for 줄 in 문단요소.text.split('\n'):
                if not 줄:
                    continue
                try:
                    _, 어절, 형태분석 = 줄.split('\t', maxsplit=2)
                except ValueError:
                    # 형태분석이 누락된 경우
                    continue
                형태분석 = 형태분석.strip()

                if not 어절:
                    continue

                형태소_품사_쌍_목록 = []
                for 형태소_품사 in 형태분석.replace(' ', '').split('+'):
                    # //SP 와 같은 경우 때문에, 정규식 활용 필요.
                    try:
                        형태소, 품사 = re.findall(r'.+(?=/)|(?<=/).+', 형태소_품사)
                    except ValueError:
                        # 형태소 또는 품사가 없는 경우
                        continue
                    
                    # 빈 형태소 제외
                    if not 형태소:
                        continue
                    # 형태소 주석 제거: 세계__02 --> 세계
                    형태소 = re.sub(r'(.+)__\d{1,}', r'\1', 형태소)
                    형태소_품사_쌍_목록.append((형태소, 품사))

                형태소_품사_쌍_목록 = tuple(형태소_품사_쌍_목록)
                # 결과 반환
                if self._어절 and self._tagged:
                    yield (어절, 형태소_품사_쌍_목록)
                elif not self._어절 and self._tagged:
                    for 형태소, 품사 in 형태소_품사_쌍_목록:
                        yield 형태소, 품사
                elif self._어절 and not self._tagged:
                    for 형태소, _ in 형태소_품사_쌍_목록:
                        yield (어절, 형태소)
                else:
                    for 형태소, _ in 형태소_품사_쌍_목록:
                        yield 형태소



class SejongSentSeq(TokenSeq):
    def __init__(self, fileids, encoding, **options):
        super().__init__(fileids, encoding)
        self._options = options

    def _get_token(self, fileid):
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
        sent_elt = body.find_all('s')

        for elt in sent_elt:
            if elt.find('note'):
                continue  # skip <note>

            if self._options.get('tagged'):
                sent = []            
                for line in elt.text.split('\n'):
                    raw_token = line.split('\t')[-2:]
                    if not raw_token[-1]:
                        continue

                    tagged_tokens = tuple(tuple(tag.split('/'))
                                        for tag in raw_token[-1].split('+'))

                    
                    sent.extend(tagged_tokens)
                yield sent

            elif self._options.get('token'):
                pieces=[]
                for line in elt.text.split('\n'):
                    raw_token = line.split('\t')[-2:]
                    if not raw_token[-1]:
                        continue
                    
                    tagged_tokens = tuple(tuple(tag.split('/'))
                                        for tag in raw_token[-1].split('+'))
                    tokens = tuple(token for token, tag in tagged_tokens)
                    pieces.extend(tokens)
                yield tuple(pieces)

            else:
                pieces=[]
                for line in elt.text.split('\n'):
                    raw_token = line.split('\t')[-2:]
                    if not raw_token[-1]:
                        continue

                    pieces.append(raw_token[0])
                yield ' '.join(pieces)
