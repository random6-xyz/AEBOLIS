FROM ubuntu:24.04

WORKDIR /root

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && apt-get update && apt-get install -y

RUN apt update && apt install -y git sudo python3 python3-pip -y
RUN python3 -m pip install --upgrade pip

RUN git clone https://github.com/random6-xyz/AEBOLIS.git "$HOME/AEBOLIS"

RUN pip install ~/AEBOLIS/requirements.txt

WORKDIR /root/AEBOLIS

ENV FLASK_SECRET_KEY "alalaalal!@lkej"
ENV PORT 7777

RUN python3 run.py