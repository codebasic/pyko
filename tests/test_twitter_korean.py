# coding: utf-8
import pytest
from pyko import OpenKoreanTextProcessor


@pytest.fixture()
def processor():
    return OpenKoreanTextProcessor()


def test_construction():
    assert OpenKoreanTextProcessor()


def test_normalize(processor):
    text = '한국어를 처리하는 예시입니닼ㅋㅋㅋㅋ'
    gold = '한국어를 처리하는 예시입니다ㅋㅋㅋ'

    text_normalized = processor.normalize(text)
    assert text_normalized == gold


def test_tokenize(processor):
    text = '한국어를 처리하는 예시입니닼ㅋㅋㅋㅋ'
    gold = ['한국어', '를', '처리', '하는', '예시', '입니다', 'ㅋㅋㅋ']

    text_normalized = processor.normalize(text)
    tokens = processor.tokenize(text_normalized)
    assert tokens == gold
