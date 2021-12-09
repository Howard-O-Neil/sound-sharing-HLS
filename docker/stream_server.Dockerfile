FROM ubuntu:18.04@sha256:fc0d6af5ab38dab33aa53643c4c4b312c6cd1f044c1a2229b2743b252b9689fc

RUN apt update
RUN apt install -y git wget software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8

RUN wget -qO - https://nginx.org/download/nginx-1.20.2.tar.gz | tar -xvz -C /usr/local/
RUN mkdir -p /usr/local/nginx-rtmp-module && \ 
    git clone https://github.com/arut/nginx-rtmp-module.git /usr/local/nginx-rtmp-module/

WORKDIR /usr/local