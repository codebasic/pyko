from setuptools import setup, find_packages


setup(
    name='pyko',
    version='0.2.0',
    description='Korean Text Processor',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    url='https://github.com/codebasic/pyko',
    keywords='natural language processing text korean',
    packages=find_packages(),
    package_data={
        'pyko': ['java/*.jar']
    },
    install_requires=['jpype1']
)
