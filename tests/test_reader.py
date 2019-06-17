import os
import re
import pytest
from pandas import DataFrame

from pyko.reader import SejongCorpusReader


@pytest.fixture
def reader():
    return SejongCorpusReader(root=ROOT, fileids=r'.+/word_tag/.+\.txt$')
    

ROOT = 'corpus/sejong/'

class TestSejong:
    def test_fileids(self):
        ROOT = 'corpus/sejong/'

        pattern = r'.+/.+/.+\.txt'
        files_regex = re.compile(ROOT + pattern)
        expected_files = []
        for root, dirs, files in os.walk(ROOT):
            for filename in files:
                filepath = os.path.join(root, filename)
                if files_regex.match(filepath):
                    expected_files.append(filepath)

        reader = SejongCorpusReader(
            root=ROOT, fileids=pattern, encoding='utf-16')

        fileids = [os.path.join(ROOT, entry) for entry in reader.fileids()]

        assert sorted(expected_files) == sorted(fileids)

    def test_tagged_words(self, reader):
        tagged_tokens = reader.words(tagged=True)
        assert len(tagged_tokens)
        for token, tags in tagged_tokens:
            assert len(tags)
            for tag in tags:
                assert len(tag) == 2

        assert tagged_tokens[0]

        assert len(tagged_tokens[:10]) == 10
        assert len(tagged_tokens[10:30]) == 20

    def test_words(self):
        reader = SejongCorpusReader(
            root='corpus/sejong',
            fileids=['spoken/word_tag/5CT_0013.txt', 'written/word_tag/BSAA0001.txt'])

        def 형태소양식(형태소):
            # 빈 형태소 포함 확인
            assert 형태소
            # 형태소 주석 제거 확인
            # 예: 세계__02 --> 세계
            assert not re.search(r'(.+)__\d{1,}', 형태소)            
        
        구어파일 = reader.fileids()[0]
        tokens = reader.words(구어파일)
        tagged_tokens = reader.words(구어파일, tagged=True)
        test_tokens = []
        for 어절, 형태분석 in tagged_tokens:
            for 형태소, 품사 in 형태분석:
                test_tokens.append(형태소)
        assert tokens[:] == test_tokens[:]

        # 문어 파일
        현대문어 = SejongCorpusReader('corpus/sejong', r'written/word_tag/.+\.txt$')
        
        for fid in 현대문어.fileids()[:10]:
            tokens = 현대문어.words(fid)[:]
            assert tokens
            
            for 형태소 in tokens:
                형태소양식(형태소)

            # words()와 words(tagged=True)의 형태소 일치 여부 확인
            어절_형태분석 = 현대문어.words(fid, tagged=True, 어절=True)[:]
            assert 어절_형태분석

            test_tokens = []
            for 어절, 형태분석 in 어절_형태분석:
                for 형태소, 품사 in 형태분석:
                    test_tokens.append(형태소)
            assert tokens == test_tokens

            기대값 = []
            for 어절, 형태분석 in 어절_형태분석:
                기대값.extend(형태분석)
            assert 기대값 == 현대문어.words(fid, tagged=True)[:]

    def test_sents(self, reader):
        sents = reader.sents()
        expected_sent = '뭐 타고 가?'
        assert expected_sent == sents[0]

    def test_tagged_sents(self, reader):
        tagged_sents = reader.tagged_sents()
        expected = [('뭐', 'NP'), ('타', 'VV'), ('고', 'EC'), ('가', 'VV'), ('ㅏ', 'EF'), ('?', 'SF')]
        assert expected == tagged_sents[0]

    def test_token_sents(self, reader):        
        expected = ('뭐', '타', '고', '가', 'ㅏ', '?')
        assert expected == reader.token_sents()[0]

    def test_tagset(self):
        tagset_frame = SejongCorpusReader.get_tagset()
        assert isinstance(tagset_frame, DataFrame)
        assert len(tagset_frame)        