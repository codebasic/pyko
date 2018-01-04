"""
Copyright (C) 2017 Codebasic
Author: Lee Seongjoo <seongjoo@codebasic.io>
"""
import itertools
import abc
import reprlib

from nltk.corpus.reader.api import CorpusReader
from bs4 import BeautifulSoup

class TokenSeq(abc.ABC):
    def __init__(self, fileids, encoding, tagged):
        self.fileids = fileids
        self.tagged = tagged
        self.encoding = encoding
                
    def __iter__(self):
        return itertools.chain(token for fid in self.fileids for token in self._get_token(fid, self.tagged))
    
    def __len__(self):
        if not hasattr(self, 'length'):
            self.length = 0
            for _ in iter(self): self.length +=1
        return self.length
        
    def __getitem__(self, index):
        it = iter(self)
        if isinstance(index, slice):
            item_it = itertools.islice(it, index.start, index.stop, index.step)
        else:
            item_it = itertools.islice(it, index, index+1)
            
        return [token for token in item_it]

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


    def words(self, fileids=None, tagged=True):
        """각 파일의 생성기 토큰을 하나의 생성기로 반환"""
        return SejongWordSeq([fid for fid in self.abspaths(fileids)], tagged=tagged)
            
                    
class SejongWordSeq(TokenSeq):
    def __init__(self, fileids, encoding='utf-16', tagged=True):
        super().__init__(fileids, encoding, tagged)
        
    def _get_token(self, fileid, tagged):
        """각 파일별 토큰 생성"""
        soup = BeautifulSoup(open(fileid, encoding=self.encoding), 'lxml')
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

