from khaiii import KhaiiiApi

_tokenizer = KhaiiiApi()

def tokenize(본문, tagged=False):
    if not 본문.strip():
        raise ValueError

    분석결과 = _tokenizer.analyze(본문)

    for 어절_형태분석 in 분석결과:
        for 요소 in 어절_형태분석.morphs:
            if tagged:
                yield 요소.lex, 요소.tag
            else:
                yield 요소.lex
