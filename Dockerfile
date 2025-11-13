FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9527 9528 9529

ENTRYPOINT ["python3", "app.py"]