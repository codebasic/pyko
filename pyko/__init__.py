# coding: utf-8
import os
from pkg_resources import resource_filename

from jpype import getDefaultJVMPath
import jpype


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
