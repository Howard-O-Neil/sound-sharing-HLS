FROM ubuntu:18.04@sha256:fc0d6af5ab38dab33aa53643c4c4b312c6cd1f044c1a2229b2743b252b9689fc

# some tools
RUN apt update
RUN apt install -y git wget software-properties-common ffmpeg

# configure python3
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8 python3-distutils
RUN wget -qO - https://bootstrap.pypa.io/get-pip.py | python3
RUN python3 -m pip install flask python-dotenv

RUN mkdir /mnt/cdn

COPY startup.sh /home/root/
WORKDIR /home/root/

RUN chmod +x startup.sh

ENTRYPOINT [ "tail", "-f", "/home/root/container_share.log" ]