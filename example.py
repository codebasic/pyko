# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pyko.reader import SejongCorpusReader

reader = SejongCorpusReader(
        'corpus/sejong', 'spoken/word_tag/.+\.txt', encoding='utf-16')

print('\nwords()')
tokens = reader.words()
print(tokens[0])
print(tokens[:10])

print('\nwords(tagged=True)')
tagged_tokens = reader.words(tagged=True)
print(tagged_tokens[0])
print(tagged_tokens[:10])

print('\nsents()')
sents = reader.sents()
print(sents[0])
print(sents[:5])

print('\nsents(tagged=True)')
tagged_sents = reader.sents(tagged=True)
print(tagged_sents[0])
print(tagged_sents[:5])