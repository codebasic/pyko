
from random import choice
import types
import numpy as np
from pandas import Series
import pytest

from pyko.reader import SejongCorpusReader
from pyko import WordSet

@pytest.fixture
def reader():
    reader = SejongCorpusReader(
        'corpus/sejong', r'(spoken|written)/word_tag/.+\.txt$')
    return reader

class TestWordSet:
    def test_build_word_set(self, reader):        
        tokens = reader.words(reader.fileids()[:10])
        word_set = WordSet(tokens)
        assert len(word_set) > 0
        # 고유 단어 집합 확인
        assert len(word_set) == len(np.unique(word_set.word_set)) 
        assert word_set[0] == 'UNK' # 없는 단어 색인 0
        assert all(word_set[1:] == sorted(word_set[1:]))

    def test_get_word_index(self, reader):
        tokens = reader.words(reader.fileids()[0])
        word_set = WordSet(tokens)
        sample_word = choice(word_set[1:])
        assert word_set.get_word_index(sample_word) > 0
        UNK_WORD = '쀍'
        assert word_set.get_word_index(UNK_WORD) == 0
        
        matched = word_set.get_word_index(pattern='나')
        assert isinstance(matched, dict)
        assert len(matched) > 1
        assert word_set.get_word_index(pattern='쀍') == 0

    def test_text_to_word_id_sequence(self, reader):
        word_set = WordSet(reader.words(reader.fileids()[0]))
        texts = reader.token_sents()[:10]
        word_index_seqs = word_set.text_to_word_id_sequence(texts)
        assert isinstance(word_index_seqs, types.GeneratorType)
        assert len(texts) == len(list(word_index_seqs))

        for seq in word_index_seqs:
            for wid in seq:
                assert wid < len(word_set)

    def test_skipgram(self, reader):
        word_set = WordSet(reader.words(reader.fileids()[0]))
        texts = reader.token_sents()[:10]
        skipgram_pairs = word_set.generate_skipgrams(texts)
        assert isinstance(skipgram_pairs, types.GeneratorType)
        for pairs, labels in skipgram_pairs:        
            x = np.array(pairs)
            assert x.ndim == 2
            assert x.shape[1] == 2
            assert all(np.isin(labels, [0, 1]))

    def test_cbow(self, reader):
        word_set = WordSet(reader.words(reader.fileids()[0]))
        texts = reader.token_sents()[:10]

        def validate_cbow(cbow, window_size, negative_samples):
            labels = []
            for pairs in cbow:
                for (context_wids, target_wid), label in pairs:
                    labels.append(label)
                    assert len(context_wids) == 2*window_size
                    assert target_wid == int(target_wid)
            
            # negative samples check
            if negative_samples:
                label_freq = Series(labels).value_counts()
                assert len(label_freq) > 1
                assert int(label_freq[1] * negative_samples) == label_freq[0]
        
        negative_samples = 0.0
        for window_size in range(1, 5):
            cbow = word_set.generate_cbow(
                texts, window_size, negative_samples)            
            validate_cbow(cbow, window_size, negative_samples)

        negative_samples = 1.0
        for window_size in range(1, 5):
            cbow = word_set.generate_cbow(
                texts, window_size, negative_samples)            
            validate_cbow(cbow, window_size, negative_samples)

        negative_samples = 0.3
        for window_size in range(1, 5):
            cbow = word_set.generate_cbow(
                texts, window_size, negative_samples)            
            validate_cbow(cbow, window_size, negative_samples)

        negative_samples = 3.3
        for window_size in range(1, 5):
            cbow = word_set.generate_cbow(
                texts, window_size, negative_samples)            
            validate_cbow(cbow, window_size, negative_samples)
