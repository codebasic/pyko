# pyko

pyko[파이코]는 한국어 텍스트 처리를 위한 파이썬 라이브러리입니다. 자연어 처리에서 한국어가 갖는 독자적인 특징을
반영해 처리합니다.

## 설치

PyPI에 등록된 패키지를 다음과 같이 설치할 수 있습니다.

    pip install pyko

## 세종말뭉치

[세종말뭉치](https://www.korean.go.kr/nkview/nklife/2016_2/26_0204.pdf)를 NLTK CorpusReader를 활용하는 것과 유사하게 활용할 수 있습니다. 세종말뭉치는 [국립국어원 언어정보나눔터](https://ithub.korean.go.kr/)에서 획득할 수 있습니다.

사용예시:

```python
from pyko.reader import SejongCorpusReader

세종말뭉치 = SejongCorpusReader(root, fileids)
파일목록 = 세종말뭉치.fileids()

형태분석목록 = 세종말뭉치.words(tagged=True)
print(형태분석목록)
"""
[('뭐', (('뭐', 'NP'),)), ('타고', (('타', 'VV'), ('고', 'EC'))), ('가?', (('가', 'VV'), ('ㅏ', 'EF'), ('?', 'SF'))), ('지하철.', (('지하철', 'NNG'), ('.', 'SF'))), ('기차?', (('기차', 'NNG'), ('?', 'SF'))), ('아침에', (('아침', 'NNG'), ('에', 'JKB'))), ...]
"""

형태분석문장목록 = 세종말뭉치.sents(tagged=True)
print(형태분석문장목록[0])
"""
[('뭐', (('뭐', 'NP'),)),
 ('타고', (('타', 'VV'), ('고', 'EC'))),
 ('가?', (('가', 'VV'), ('ㅏ', 'EF'), ('?', 'SF')))]
"""
```

## 형태소 분리 및 품사 예측

### v0.4.0+
형태소 분석기는 딥러닝 기반의 카카오 형태소 분석기, [kakao/khaiii](https://github.com/kakao/khaiii)를 내부적으로 활용합니다. 해당 패키지가 시스템에 설치된 것을 가정합니다.

모든 환경이 미리 설정된 도커(docker) 이미지를 활용하면 편리합니다.

pyko 도커 이미지: [codebasic/pyko](https://hub.docker.com/repository/docker/codebasic/pyko)

도커 이미지 사용 예시

```
$ docker run -it codebasic/pyko
```

사용예시:

```python
from pyko import tokenizer as 형태소_분석기

예문 = '한국어를 잘 처리하는지 궁금합니다.'
분석결과 = 형태소_분석기.tokenize(예문)
print(list(분석결과))
"""
['한국어', '를', '잘', '처리', '하', '는지', '궁금', '하', 'ㅂ니다', '.']
"""
```
