ffmpeg -re -stream_loop -1 \
    -i ab/TalkingMachinesPodcast-a348dacf-86af-4e80-9aba-17fa7aad9158.wav \
    -vcodec libx264 \
    -vprofile baseline \
    -g 30 -acodec aac \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound1

ffmpeg -re -stream_loop -1 \
    -i ab/Symphony_No.6_1st_movement-8950f11f-f22f-46e9-9da1-2c5c95d0a890.mp3 \
    -vcodec libx264 \
    -vprofile baseline \
    -g 30 -acodec aac \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound1

ffmpeg -re -stream_loop -1 \
    -i ab/1639128337876-26898697-26fe-4bd2-baf6-9b4a31ee1d54.mp4 \
    -c:v libx264 \
    -b:v 2M -c:a copy \
    -strict -2 -flags +global_header \
    -bsf:a aac_adtstoasc \
    -bufsize 2100k \
    -f flv rtmp://128.0.3.2:1935/show/sound2

ffmpeg -re -i ab/1639128337876-26898697-26fe-4bd2-baf6-9b4a31ee1d54.mp4 \
        -bsf:v h264_mp4toannexb \
        -c copy -f mpegts rtmp://128.0.3.2:1935/show/vid1

ffmpeg -re -stream_loop -1 \
    -i /mnt/cdn/ab/1639128337876-26898697-26fe-4bd2-baf6-9b4a31ee1d54.mp4 \
    -vcodec copy -c:a aac -b:a 160k -ar 44100 \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound2

ffmpeg -re -stream_loop -1 \
    -i /mnt/cdn/ab/Symphony_No.6_1st_movement-8950f11f-f22f-46e9-9da1-2c5c95d0a890.mp3 \
    -vcodec copy -c:a aac -b:a 160k -ar 44100 \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound2