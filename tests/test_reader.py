import os
import pytest
from pyko.reader import SejongCorpusReader


CORPUS_ROOT = os.environ['CORPUS_ROOT']
SEJONG_CORPUS_PATH = os.path.join(CORPUS_ROOT, 'sejong')

@pytest.fixture(scope='module', params=[r'spoken/word_tag/.+\.txt'])
def 세종말뭉치(request):
    return SejongCorpusReader(SEJONG_CORPUS_PATH, request.param)
        
def test_words(세종말뭉치):
    형태분석목록 = 세종말뭉치.words(tagged=True)
    assert len(형태분석목록)
    
    for 어절, 형태분석 in 형태분석목록:
        assert 어절
        assert len(형태분석)
        for 형태소, 품사 in 형태분석:
            assert 형태소
            assert 품사
        