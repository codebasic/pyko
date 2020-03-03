import inspect
import pytest

from pyko.tokenizer import 카카오_카이

def test_tokenize():
    형태소_분석기 = 카카오_카이()
    예문 = '한국어를 잘 처리하는지 궁금합니다.'
    형태소_목록 = 형태소_분석기.tokenize(예문)
    assert inspect.isgenerator(형태소_목록)

    expected = ['한국어', '를', '잘', '처리', '하', '는지', '궁금', '하', 'ㅂ니다', '.']
    assert list(형태소_목록) == expected

    # 빈 문자열 처리
    with pytest.raises(ValueError):
        list(형태소_분석기.tokenize(''))