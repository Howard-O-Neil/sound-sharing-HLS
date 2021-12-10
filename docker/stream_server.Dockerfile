FROM ubuntu:18.04@sha256:fc0d6af5ab38dab33aa53643c4c4b312c6cd1f044c1a2229b2743b252b9689fc

# some tools
RUN apt update
RUN apt install -y git wget software-properties-common

# nginx essentials
RUN apt install -y build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev

# configure nginx
RUN wget -qO - https://nginx.org/download/nginx-1.20.2.tar.gz | tar -xvz -C /usr/local/
RUN mkdir -p /usr/local/nginx-rtmp-module && \ 
    git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git /usr/local/nginx-rtmp-module/

WORKDIR /usr/local/nginx-1.20.2

RUN mkdir -p /mnt/hls 

RUN ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
RUN make -j 1
RUN make install

# apply configuration
COPY nginx.conf /home/root/
WORKDIR /home/root/

RUN cat nginx.conf > /usr/local/nginx/conf/nginx.conf

ENTRYPOINT [ "/usr/local/nginx/sbin/nginx" ]