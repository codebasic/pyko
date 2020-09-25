import os
from setuptools import setup, find_packages

with open('README.md', encoding='utf8') as f:
    문서 = f.read()

setup(
    name='pyko',
    version=os.environ['VERSION'],
    description='Korean Text Processor',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    url='https://github.com/codebasic/pyko',
    keywords='natural language processing text korean',
    packages=find_packages(),
    install_requires=['nltk', 'beautifulsoup4', 'lxml'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: Korean',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X'
    ],
    long_description=문서,
    long_description_content_type="text/markdown",
    python_requires='>=3.4'
)
