FROM codebasic/pyko

# 컨테이너 시작 시, 주피터 노트북 바로 실행
RUN conda install -y jupyter
CMD ["jupyter", "notebook", "--notebook-dir='/notebooks'", "--ip='*'", "--no-browser", "--allow-root"]
