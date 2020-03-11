FROM codebasic/khaiii

RUN pip install nltk pandas matplotlib scikit-learn lxml

ENV WORKDIR=/workspaces
WORKDIR ${WORKDIR}

ENV DIST_FILE=pyko-0.4.1-py3-none-any.whl
COPY dist/${DIST_FILE} .
RUN pip install ${DIST_FILE}
RUN rm ${DIST_FILE}
