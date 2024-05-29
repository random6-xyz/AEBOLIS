FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /root

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && apt-get update && apt-get install -y

RUN apt update && apt install -y git sudo python3 python3-pip libffi-dev build-essential libssl-dev libc6-i386 libc6-dbg gcc-multilib make -y
RUN python3 -m pip install pip 


RUN git clone https://github.com/random6-xyz/AEBOLIS.git /root/AEBOLIS

RUN pip install -r ~/AEBOLIS/requirements.txt

WORKDIR /root/AEBOLIS

ENV FLASK_SECRET_KEY "alalaalal!@lkej"
ENV PORT 7777

CMD ["python3", "run.py"]