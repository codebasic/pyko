FROM codebasic/khaiii

RUN pip install nltk pandas matplotlib scikit-learn lxml

ENV WORKDIR=/workspaces
WORKDIR ${WORKDIR}
RUN mkdir pyko
COPY . pyko
RUN pip install -e pyko
