PKG_VERSION=`python -c "import pyko; print(pyko.__version__)"`
if [ $PKG_VERSION == $VERSION ]; then
    python setup.py sdist bdist_wheel
else
    echo "패키지 버전이 환경 변수 설정과 다릅니다."
fi
