FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"] 