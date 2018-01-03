import os
import re
import pytest
from pyko.reader import SejongCorpusReader


class TestSejong:
    def test_fileids(self):
        ROOT = '../corpus/sejong/'

        pattern = '.+/.+/.+\.txt'
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

    @pytest.mark.skip()
    def test_sents(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/spoken/raw',
            fileids=['4CM00003.txt', '4CM00005.txt'],
            encoding='utf-16')
        assert sejong.sents()

    @pytest.mark.skip()
    def test_words(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/spoken/word_tag',
            fileids=['5CT_0013.txt', '5CT_0014.txt'],
            encoding='utf-16')
        assert sejong.words(tagged=True)

    @pytest.mark.skip()
    def test_sents_from_tagged(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/spoken/word_tag',
            fileids=['5CT_0013.txt', '5CT_0014.txt'],
            encoding='utf-16')
        assert sejong.sents(tagged=True)

    @pytest.mark.skip()
    def test_regex_fileids(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/',
            fileids='*.txt',
            encoding='utf-16'
        )

        for fid in sejong.fileids():
            if not fid.endswith('.txt'):
                assert False
