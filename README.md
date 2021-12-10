# sound-sharing-HLS
HLS Stream server, CDN

## Stream server architecture
![picture 1](images/d02db075706a4b0f486923990fdcf8282ded36674f728fb966bf1d82ee73b836.png)

Our stream server is implemented in nginx

Basically, we have our cdn stream content through ffmpeg. The cdn itself support endpoints to stream and end-stream its content