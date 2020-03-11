pypirc=$1
dist=$2

cp $pypirc $HOME
python -m twine upload $dist
