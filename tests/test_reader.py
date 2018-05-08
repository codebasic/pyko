import os
import re
import pytest
from pyko.reader import SejongCorpusReader

@pytest.fixture
def reader():
    reader = SejongCorpusReader(
        'corpus/sejong', r'spoken/word_tag/.+\.txt', encoding='utf-16')
    return reader

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
        tokens = reader.words()
        tagged_tokens = reader.words(tagged=True)
        test_tokens = [word for raw, token in tagged_tokens for word, tag in token]
        assert tokens[:] == test_tokens[:]
            