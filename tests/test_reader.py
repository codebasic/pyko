import os
import re
import pytest

from pyko.reader import SejongCorpusReader


CORPUS_ROOT = os.environ['CORPUS_ROOT']
SEJONG_CORPUS_PATH = os.path.join(CORPUS_ROOT, 'sejong')

@pytest.fixture(scope='module', 
    params=[r'spoken/word_tag/.+\.txt', r'written/word_tag/.+\.txt'])
def 세종말뭉치(request):
    return SejongCorpusReader(SEJONG_CORPUS_PATH, request.param)
        
def test_fileids(세종말뭉치):
    assert 세종말뭉치.fileids()
    
def test_words(세종말뭉치):
    형태분석목록 = 세종말뭉치.words(tagged=True)
    assert len(형태분석목록)
    
    for 어절, 형태분석 in 형태분석목록:
        assert 어절
        assert len(형태분석)
        for 형태소, 품사 in 형태분석:
            assert 형태소
            assert 품사

            # 형태소 뒷번호 정리 확인 예: 세계__02 --> 세계
            assert not re.search(r'__\d{1,}', 형태소)
        
def test_sents(세종말뭉치):
    형태분석문장목록 = 세종말뭉치.sents(tagged=True)
    # 예: ['프랑스의', '세계적인', '의상', '디자이너', '엠마누엘', '웅가로가', '실내', '장식용', '직물', '디자이너로', '나섰다.']
    원시문장목록 = 세종말뭉치.sents(tagged=False)
    """
    예: ['프랑스', ' 의', '세계', ' 적', '이', 'ᆫ', '의상', '디자이너', '엠마누엘', '웅가로', '가',
    '실내', '장식', '용', '직물', '디자이너', '로', '나서', '었', '다','.']
    """
    형태분리문장목록 = 세종말뭉치.sents(tagged=False, 형태분리=True)

    assert len(형태분석문장목록) == len(원시문장목록) == len(형태분리문장목록)

    for 형태분석문장, 원시문장, 형태분리문장 in zip(형태분석문장목록, 원시문장목록, 형태분리문장목록):
        assert 형태분석문장
        assert 원시문장
        assert 형태분리문장

        어절목록 = [어절 for 어절, 형태분석 in 형태분석문장]
        형태소목록 = [형태소 for 어절, 형태분석 in 형태분석문장 for 형태소, 품사 in 형태분석]
        assert 어절목록 == 원시문장
        assert 형태소목록 == 형태분리문장