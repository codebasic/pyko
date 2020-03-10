import os
import re
import pytest
from pyko.reader import SejongCorpusReader


class TestSejong:
    CORPUS_ROOT = os.environ['CORPUS_ROOT']
    CORPUS_PATH = os.path.join(CORPUS_ROOT, 'sejong')
        
    def test_words(self):        
        reader = SejongCorpusReader(
                TestSejong.CORPUS_PATH, 
                r'spoken/word_tag/.+\.txt', encoding='utf-16')
        
        형태분석목록 = reader.words(tagged=True)
        assert len(형태분석목록)
        
        for 어절, 형태분석 in 형태분석목록:
            assert 어절
            assert len(형태분석)
            for 형태소, 품사 in 형태분석:
                assert 형태소
                assert 품사
        