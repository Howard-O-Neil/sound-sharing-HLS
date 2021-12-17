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

ffmpeg -re \
    -i /mnt/cdn/ab/1639684848378.mp4 \
    -vcodec copy -preset ultrafast -c:a aac -b:a 160k -ar 44100 \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound2

ffmpeg -re -stream_loop -1 \
    -i /mnt/cdn/ab/Symphony_No.6_1st_movement-8950f11f-f22f-46e9-9da1-2c5c95d0a890.mp3 \
    -vcodec copy -c:a aac -b:a 160k -ar 44100 \
    -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound2 2> /dev/null &

VIDSOURCE="rtsp://192.1xx.x.xxx:5554"
AUDIO_OPTS="-c:a aac -b:a 160000 -ac 2"
VIDEO_OPTS="-s 854x480 -c:v libx264 -b:v 800000"
OUTPUT_HLS="-hls_time 10 -hls_list_size 10 -start_number 1"
ffmpeg -re -stream_loop -1 -i /mnt/cdn/ab/1639684848378.mp4 \
    -y -c:a aac -b:a 160000 -ac 2 \
    -s 854x480 -c:v libx264 -b:v 800000 \
    -hls_time 10 -hls_list_size 10 -start_number 1 /mnt/cdn/ab/playlist.m3u8


ffmpeg -re -stream_loop -1 -i /mnt/cdn/ab/1639684848378.mp4 \
    -vcodec copy -loop -1 \
    -b:v 1600k -preset ultrafast \
    -b 900k -c:a aac -b:a 128k -s 1920×1080 -x264opts keyint=50 -ar 44100 \
    -g 25 -pix_fmt yuv420p -strict -2 -f flv rtmp://128.0.3.2:1935/show/sound2

# ffmpeg -re -stream_loop -1 -i /mnt/cdn/ab/1639684848378.mp4 -v 0 -vcodec mpeg4 -f mpegts rtmp://128.0.3.2:1935/show/sound2

# ffmpeg -re -stream_loop -1 -f lavfi -i /mnt/cdn/ab/1639684848378.mp4 -vcodec copy\
#     -c:v libx264 \
#     -b:v 1600k -preset ultrafast \
#     -b 900k -c:a libfdk_aac -b:a 128k -s 1920×1080 -x264opts keyint=50 \
#     -g 25 -pix_fmt yuv420p -f flv rtmp://128.0.3.2:1935/show/sound2