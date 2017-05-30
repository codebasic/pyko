# coding: utf-8
import pytest
from pyko import OpenKoreanTextProcessor


@pytest.fixture(scope='module')
def processor():
    return OpenKoreanTextProcessor()


class TestOpenKoreanTextProcessor:
    text = '한국어를 처리하는 예시입니닼ㅋㅋㅋㅋ'

    def test_construction(self):
        assert OpenKoreanTextProcessor()

    def test_normalize(self, processor):
        gold = '한국어를 처리하는 예시입니다ㅋㅋㅋ'
        text_norm = processor.normalize(self.text)
        assert text_norm == gold

    def test_tokenize(self, processor):
        gold = ['한국어', '를', '처리', '하는', '예시', '입니다', 'ㅋㅋㅋ']
        text_norm = processor.normalize(self.text)
        tokens = processor.tokenize(text_norm)
        assert tokens == gold

    @pytest.mark.skip(reason='Depedency library does not support')
    def test_stem(self, processor):
        gold = ['한국어', '를', '처리', '하다', '예시', '이다', 'ㅋㅋㅋ']
        text_norm = processor.normalize(self.text)
        stem_tokens = processor.stem(text_norm)
        assert stem_tokens == gold
