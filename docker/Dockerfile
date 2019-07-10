# $ cd fract
# $ docker build -f docker/Dockerfile -t fract/dev .

FROM python:3.6-slim

COPY requirements.txt requirements.txt

RUN apt update && apt -y install vim dnsutils git \
      && apt clean \
      && rm -rf /var/lib/apt/lists/* \ 
      && pip install -r requirements.txt \
      && rm -rf /root/.cache 

RUN mkdir -p /fract/src
COPY ./src /fract/src/
COPY fract /fract/
COPY sprett /fract/

ENV PYTHONPATH /fract/src/
ENV PATH="/fract/:${PATH}"

