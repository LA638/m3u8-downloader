# m3u8-downloader

* Multithread downloading of audio and video streams.
* Requires [ffmpeg](https://www.ffmpeg.org/) to merge .ts video file and .aac audio file into .mp4 file.
* To use add **.env** file with following parameters.
It must looks like this:
```
M3U8_VIDEO_PLAYLIST_URL=https://video_playlist_url/720p.m3u8
M3U8_AUDIO_PLAYLIST_URL=https://audio_playlist_url/Audio0.m3u8
M3U8_OUTPUT_PATH=out/
M3U8_OUTPUT_VIDEOFILE=720p.ts
M3U8_OUTPUT_AUDIOFILE=Audio0.aac
M3U8_OUTPUT_FILE=my_video.mp4