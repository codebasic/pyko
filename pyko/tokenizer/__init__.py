# 카카오 형태소 분석기
try:
    from khaiii import KhaiiiApi
except:
    raise ImportError('카카오 형태소 분석기 설치가 필요합니다.')

class 카카오_카이:
    def __init__(self):
        self.tokenizer = KhaiiiApi()

    def tokenize(self, 본문, tagged=False):
        if not 본문.strip():
            raise ValueError
        
        분석결과 = self.tokenizer.analyze(본문)

        for 어절_형태분석 in 분석결과:
            for 요소 in 어절_형태분석.morphs:
                if tagged:
                    yield 요소.lex, 요소.tag
                else:
                    yield 요소.lex
