from setuptools import setup, find_packages


setup(
    name='pyko',
    version='0.1',
    description='Korean Text Processor',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    url='https://github.com/codebasic/pyko',
    keywords='natural language processing text korean'
    packages=find_packages(),
    package_data={
        'pyko': ['java/*.jar']
    },
    classifiers=[
        'Classifier: Development Status :: 3 - Alpha',
        'Classifier: License :: OSI Approved :: Apache Software License',
        'Classifier: Natural Language :: Korean',
        'Classifier: Operating System :: MacOS',
        'Classifier: Operating System :: Microsoft :: Windows',
        'Classifier: Programming Language :: Java',
        'Classifier: Programming Language :: Python :: 3',
        'Classifier: Topic :: Scientific/Engineering',
        'Classifier: Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Classifier: Topic :: Software Development :: Libraries :: Java Libraries',
        'Classifier: Topic :: Software Development :: Version Control :: Git',
        'Classifier: Topic :: Text Processing',
        'Classifier: Topic :: Text Processing :: Linguistic'
    ]
)
