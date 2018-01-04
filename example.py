# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import itertools
from pyko.reader import SejongCorpusReader

reader = SejongCorpusReader(
        'corpus/sejong', 'spoken/word_tag/.+\.txt', encoding='utf-16')

token_generator = reader.words(tagged=True)

tagged_tokens = [t for t in itertools.islice(token_generator, 0, 50)]
