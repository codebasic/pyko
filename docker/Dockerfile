FROM codebasic/khaiii

WORKDIR /workspaces

ENV DIST_FILE=pyko-0.4.2-py3-none-any.whl
COPY ${DIST_FILE} .
RUN pip install ${DIST_FILE}
RUN rm ${DIST_FILE}

WORKDIR /
RUN rm -rf /workspaces
