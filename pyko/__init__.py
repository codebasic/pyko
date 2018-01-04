# coding: utf-8
import os
import re

from pkg_resources import resource_filename


from jpype import getDefaultJVMPath
import jpype

from . import reader

__all__ = [reader]

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
        raise NotImplemented('Dependency API change pending')
