FROM tensorflow/tensorflow:latest-py3 AS base

WORKDIR /workspaces/pyko
COPY . .

RUN pip install ./khaiii-0.4-py3-none-any.whl 
# Khaiii 시스템 언어 설정
RUN apt-get update -y && apt-get install -y language-pack-ko \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8

FROM base as development
RUN VERSION=0.4.2 pip install -e .

FROM base as production
RUN VERSION=0.4.2 python setup.py sdist bdist_wheel
RUN pip install dist/pyko-0.4.2-py3-none-any.whl

WORKDIR /
RUN rm -rf /workspaces
