# sound-sharing-HLS
HLS Stream server, CDN

## Stream server architecture
![picture 1](images/d02db075706a4b0f486923990fdcf8282ded36674f728fb966bf1d82ee73b836.png)

Our stream server is implemented in nginx

Basically, we have our cdn stream content to stream server through ffmpeg. 

We still using pretty dump ass approach, using bash to control ffmpeg, run the bash command in python :)))

The cdn itself support endpoints to stream and end-stream its content

## Some short demo
https://user-images.githubusercontent.com/64292857/145566213-02747836-6052-4399-8a38-febaf6444ae1.mp4

https://user-images.githubusercontent.com/64292857/145612598-e0b85cd5-f6f7-4e95-a81d-e77f0853dc33.mp4
