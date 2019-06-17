# coding: utf-8
import os
import re

from pkg_resources import resource_filename

import numpy as np
import pandas as pd
from pandas import Series
from keras.preprocessing.sequence import skipgrams

from pyko.reader import SejongCorpusReader


__version__ = '0.4.0'


def preprocessor(text):
    #비문자제거패턴 = re.compile(r'[^ㄱ-ㅣ가-힣a-zA-Z0-9 ]')
    # ㄷㄷ, ㅋㅋ 과 같은 단어는 선택에서 제외
    비문자제거패턴 = re.compile(r'[^가-힣a-zA-Z0-9 ]')
    text = 비문자제거패턴.sub('', text)
    return text


def java_str(func):
    def wrapper(self, text):
        text = jpype.java.lang.String(text)
        return func(self, text)
    return wrapper


class OpenKoreanTextProcessor:
    def __init__(self):
        from jpype import getDefaultJVMPath
        import jpype

        if not jpype.isJVMStarted():
            libpath = resource_filename(__name__, 'java')
            jars = os.listdir(libpath)
            jars = [os.path.join(libpath, item) for item in jars]
            jvm_arg = '-Djava.class.path={}'.format(os.pathsep.join(jars))

            jpype.startJVM(getDefaultJVMPath(), jvm_arg)

        self._processor = jpype.JClass(
            'org.openkoreantext.processor.OpenKoreanTextProcessorJava')

    @java_str
    def normalize(self, text):
        return self._processor.normalize(text)

    @java_str
    def tokenize(self, text):
        tokens = self._processor.tokenize(text)
        tokens = self._processor.tokensToJavaStringList(tokens)
        tokens = [t for t in tokens]
        return tokens

    @java_str
    def stem(self, text):
        raise NotImplementedError('Dependency API change pending')


class WordSet:
    def __init__(self, texts, tokenizer=None, select='^[ㄱ-ㅣ가-힣0-9]+'):
        self.select = select      
        # 0번 색인은 UNK(모름, 없음)으로 예약
        self.word_set = ['UNK']
        if tokenizer:
            tokens = tokenizer.tokenize(texts)
        else:
            tokens = texts
        self._build_word_set(tokens, select=select)
        
    def __repr__(self):
        return repr(self.word_set)
    
    def __len__(self):
        return len(self.word_set)
    
    def __getitem__(self, i):
        return self.word_set[i]
    
    def _build_word_set(self, tokens, select):
        vocab = []
        for token in tokens:
            if re.match(select, token) and not token in vocab:
                vocab.append(token)
        vocab.sort()
        self.word_set += vocab
        self.word_set = Series(self.word_set)

    def get_word_index(self, word=None, pattern=None):
        if word:
            matched = self.word_set[self.word_set == word]
            return matched.index[0] if len(matched) else 0
        
        elif pattern:
            matched = self.word_set[self.word_set.str.match(pattern)]
            return dict(matched) if len(matched) else 0

        else:
            raise ValueError('word 또는 pattern 둘 중에 하나를 지정해야 합니다.')
        
    def text_to_word_id_sequence(self, texts, select=None):
        pattern = select if select else self.select        
        for text in texts:
            id_seq = [self.get_word_index(token) for token in text if re.match(pattern, token)]
            yield id_seq
            
    def generate_skipgrams(self, texts, window_size=4, negative_samples=1.0, shuffle=True):
        vocab_size = len(self.word_set)
        word_index_seqs = self.text_to_word_id_sequence(texts)
        for wid_seq in word_index_seqs:
            if len(wid_seq) < 2:
                continue
            pairs, labels = skipgrams(wid_seq, vocab_size, 
                window_size, negative_samples, shuffle)            
            yield pairs, labels

    def generate_cbow(self, texts, window_size=1, negative_samples=1.0, verbose=False):        
        vector_length = 2*window_size + 1
        word_index_seqs = self.text_to_word_id_sequence(texts)

        n_positive_samples = 0
        for wid_seq, text in zip(word_index_seqs, texts):
            if verbose:
                print(text)
            # generate postive cbows for a sequence
            positive_pairs = []
            for start in range(len(wid_seq)-vector_length):
                context_wids = wid_seq[start:start+vector_length]
                target_wid = context_wids.pop(int(vector_length/2)) # center wid
                pos_pair = ((context_wids, target_wid), 1)                
                positive_pairs.append(pos_pair)               
                if verbose:
                    context_words = [f'{self.word_set[wid]}({wid})' for wid in context_wids]
                    target_word = f'{self.word_set[target_wid]}({target_wid})'                    
                    print(f'\t({context_words}, {target_word}) -> 1')
            yield positive_pairs
            n_positive_samples += len(positive_pairs)               

        # negative sample generation
        negative_pairs = []
        n_negative_samples = int(n_positive_samples * negative_samples)
        while len(negative_pairs) < n_negative_samples:
            # randomly select 2*window_size + 1 words from vocabulary
            # without replacement.
            context_words = self.word_set.sample(vector_length)
            context_wids = [self.get_word_index(word) for word in context_words]
            target_wid = context_wids.pop(int(vector_length/2))
            pair_candidate = (context_wids, target_wid)            
            # check duplicates
            if (not (pair_candidate, 1) in positive_pairs 
                and not (pair_candidate, 0) in negative_pairs):
                negative_pairs.append((pair_candidate, 0))                     

        yield negative_pairs
            