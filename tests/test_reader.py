import os
import re
import pytest
from pyko.reader import SejongCorpusReader


class TestSejong:
    CORPUS_ROOT = os.environ['CORPUS_ROOT']
    CORPUS_PATH = os.path.join(CORPUS_ROOT, 'sejong')
        
    def test_words(self):        
        reader = SejongCorpusReader(
                TestSejong.CORPUS_PATH, r'spoken/word_tag/.+\.txt', encoding='utf-16')
        형태분석목록 = reader.words(tagged=True)
        
        assert len(형태분석목록)
        
        for 어절, 형태분석 in 형태분석목록:
            assert len(형태분석)
            for tag in 형태분석:
                assert len(tag) == 2

        assert 형태분석목록[0]
        
        assert len(형태분석목록[:10]) == 10
        assert len(형태분석목록[10:30]) == 20