# coding: utf-8
import os
import re

from pkg_resources import resource_filename

import numpy as np
import pandas as pd
from pandas import Series
from keras.preprocessing.sequence import skipgrams

from . import reader

__all__ = [reader]
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
            
    def generate_skipgrams(self, texts):
        vocab_size = len(self.word_set)
        word_index_seqs = self.text_to_word_id_sequence(texts)
        for wid_seq in word_index_seqs:
            if len(wid_seq) < 2:
                continue
            pairs, labels = skipgrams(wid_seq, vocab_size)            
            yield pairs, labels