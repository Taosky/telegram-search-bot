FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN apt update && apt install gcc -y && apt clean
RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"] 

