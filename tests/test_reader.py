import pytest
from pyko.reader import SejongCorpusReader


class TestSejong:
    def test_fileids(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/spoken/raw',
            fileids=['4CM00003.txt', '4CM00005.txt'],
            encoding='utf-16')
        assert sejong.fileids()

    def test_sents(self):
        sejong = SejongCorpusReader(
            root='../corpus/sejong/spoken/raw',
            fileids=['4CM00003.txt', '4CM00005.txt'],
            encoding='utf-16')
        assert sejong.sents()
