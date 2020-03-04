# coding: utf-8
import os
import re

from pkg_resources import resource_filename

from . import reader

__all__ = [reader]

def preprocessor(text):
    #비문자제거패턴 = re.compile(r'[^ㄱ-ㅣ가-힣a-zA-Z0-9 ]')
    # ㄷㄷ, ㅋㅋ 과 같은 단어는 선택에서 제외
    비문자제거패턴 = re.compile(r'[^가-힣a-zA-Z0-9 ]')
    text = 비문자제거패턴.sub('', text)
    return text