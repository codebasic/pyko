"""
Copyright (C) 2017-2018 Codebasic

Author: Lee Seongjoo <seongjoo@codebasic.io>
"""
import itertools
import abc
import reprlib

from nltk.corpus.reader import CorpusReader
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

    def words(self, fileids=None, tagged=False):
        """
        말뭉치로부터 토큰 획득

        :param fileids: 말뭉치 파일 ID
        :type fileids: list[str] or None
        :return: 토큰 생성기
        :rtype: generator
        """
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, tagged=tagged)

    def sents(self, fileids=None, **options):
        return SejongSentSeq([fid for fid in self.abspaths(fileids)], encoding=self._encoding, **options)

    def tagged_sents(self, fileids=None):
        return self.sents(fileids, tagged=True)

    def token_sents(self, fileids=None):
        return self.sents(fileids, token=True)


class SejongWordSeq(TokenSeq):
    def __init__(self, fileids, encoding, tagged):
        super().__init__(fileids, encoding)
        self._tagged = tagged

    def _get_token(self, fileid):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
        body = soup.find('text')
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
