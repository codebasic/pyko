from setuptools import setup, find_packages


setup(
    name='pyko',
    version='0.4.0',
    description='Korean Text Processor',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    url='https://github.com/codebasic/pyko',
    keywords='natural language processing text korean',
    packages=find_packages(),
    install_requires=['nltk', 'beautifulsoup4', 'lxml']
)
