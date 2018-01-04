# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pyko.reader import SejongCorpusReader

reader = SejongCorpusReader(
        'corpus/sejong', 'spoken/word_tag/.+\.txt', encoding='utf-16')

tokens = reader.words(tagged=True)

print('index')
print(tokens[0])

print('Slice')
print(tokens[:10])
