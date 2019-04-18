FROM python:3.6-slim

RUN apt update && apt -y install vim dnsutils git \
      && apt clean \
      && rm -rf /var/lib/apt/lists/* \ 
      && pip install requests grip PyYAML urllib3 \
      && rm -rf /root/.cache \
      && git clone -b release https://github.com/ktmrmshk/fract.git

ENV PYTHONPATH /fract/src/
ENV PATH="/fract/:${PATH}"




