FROM python:3.6

RUN apt-get update && apt-get -y install vim dnsutils
RUN pip install requests
RUN pip install grip
RUN pip install PyYAML
RUN pip install urllib3

RUN git clone https://github.com/ktmrmshk/fract.git
ENV PYTHONPATH /fract/src/
ENV PATH="/fract/:${PATH}"




