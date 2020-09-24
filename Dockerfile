FROM tensorflow/tensorflow:latest-py3 AS builder

WORKDIR /workspaces/pyko
COPY . .

RUN pip install ./khaiii-0.4-py3-none-any.whl \
    && VERSION=0.4.2 pip install -e .

# Khaiii 시스템 언어 설정
RUN apt-get update -y && apt-get install -y language-pack-ko \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8
