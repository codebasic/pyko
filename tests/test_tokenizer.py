import inspect
import os
import tempfile
import pytest
from nltk.corpus import PlaintextCorpusReader
from pyko import tokenizer as 형태소_분석기

def test_tokenize():
    예문 = '한국어를 잘 처리하는지 궁금합니다.'
    형태소_목록 = 형태소_분석기.tokenize(예문)

    expected = ['한국어', '를', '잘', '처리', '하', '는지', '궁금', '하', 'ㅂ니다', '.']
    assert 형태소_목록 == expected

    # 빈 문자열 처리
    assert not 형태소_분석기.tokenize('')

def test_corpus_reader():
    본문 = """세종(世宗, 1397년 5월 7일 (음력 4월 10일) ~ 1450년 3월 30일(음력 2월 17일), 재위 : 1418년 ~ 1450년)은 조선의 제4대 국왕이며 언어학자이다. 그의 업적에 대한 존경의 의미를 담은 명칭인 세종대왕(世宗大王)으로 자주 일컬어진다.
성은 이(李), 휘는 도(祹), 본관은 전주(全州), 자는 원정(元正), 아명은 막동(莫同)이었다. 묘호는 세종(世宗)이며, 시호는 영문예무인성명효대왕(英文睿武仁聖明孝大王)이고, 명나라에서 받은 시호는 장헌(莊憲)이었다. 존시를 합치면 세종장헌영문예무인성명효대왕(世宗莊憲英文睿武仁聖明孝大王)이다."""

    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf8') as fp:
        fp.write(본문)
        fp.seek(0)
        파일경로 = fp.name
        폴더 = os.path.dirname(파일경로)
        파일명 = os.path.basename(파일경로)
        # # 말뭉치 리더 생성
        reader = PlaintextCorpusReader(root=폴더, fileids=[파일명], word_tokenizer=형태소_분석기)
        # 형태소 분리 확인
        분석결과 = reader.words()
        assert 분석결과
