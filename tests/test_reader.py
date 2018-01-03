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
        
    def test_words(self):
        reader = SejongCorpusReader(
                'corpus/sejong', 'spoken/word_tag/.+\.txt', encoding='utf-16')
        tagged_tokens = reader.words(tagged=True)
        
        assert len(tagged_tokens)
        
        for token, tags in tagged_tokens:
            assert len(tags)
            for tag in tags:
                assert len(tag) == 2
