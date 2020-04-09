from typing import List
from khaiii import KhaiiiApi

_tokenizer = KhaiiiApi()

def tokenize(본문, tagged=False) -> List:
    형태분석 = []
    if not 본문.strip():
        return 형태분석

    분석결과 = _tokenizer.analyze(본문)
    for 어절_형태분석 in 분석결과:
        for 요소 in 어절_형태분석.morphs:
            if tagged:
                형태분석.append((요소.lex, 요소.tag))
            else:
                형태분석.append(요소.lex)
    return 형태분석
