#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from tqdm import tqdm


def make_directory(directory_name):
    try:
        os.mkdir(directory_name)
    except (FileExistsError, FileNotFoundError) as error:
        print(error)

def get_playlist(playlist_url):
    file_list = re.findall('^[^#].+', requests.get(playlist_url).text, flags=re.MULTILINE)
    file_url = re.search('.+\/(?=.+$)', playlist_url)[0]
    file_links = []
    for file in file_list:
        file_links.append(file_url+file)
    return file_links

def save_file(file_links, out_file):
    try: 
        with open(out_file, 'wb') as file:
            for file_link in tqdm(
            file_links, 
            unit=' files', 
            desc=out_file, 
            miniters=1,
            leave=False,
            colour='#ee1a80'):
                file_request = requests.get(file_link, stream=True)
                file.write(file_request.content)
                file.flush()
    except (FileExistsError, FileNotFoundError) as error:
        print(error)

def multi_save_file(links_lists, out_files_list):
    with ThreadPoolExecutor(2) as executor:
        executor.map(save_file, links_lists, out_files_list)

def convert_file(audio_file, video_file, output_file):
    # Ffmpeg video and audio streams to file
    command = f'ffmpeg -i {video_file} -i {audio_file} -map 0:V:0 -map 1:a:0 -c copy -f mp4 -movflags +faststart {output_file}'
    print(command)
    print(os.popen(command).read())


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    video_playlist_url = os.getenv('M3U8_VIDEO_PLAYLIST_URL')
    audio_playlist_url = os.getenv('M3U8_AUDIO_PLAYLIST_URL')
    output_path = os.getenv('M3U8_OUTPUT_PATH')
    output_video_file = os.getenv('M3U8_OUTPUT_VIDEOFILE')
    output_audio_file = os.getenv('M3U8_OUTPUT_AUDIOFILE')
    output_file = os.getenv('M3U8_OUTPUT_FILE')
    print(video_playlist_url, audio_playlist_url, output_file, sep='\n')
    # Make output directory
    make_directory(output_path)

    if audio_playlist_url:
        links = [get_playlist(audio_playlist_url), get_playlist(video_playlist_url)]
        out_files = [output_path+output_audio_file, output_path+output_video_file]
        multi_save_file(links, out_files)
        convert_file(out_files[0], out_files[1], output_path+output_file)
    else: 
        save_file(get_playlist(video_playlist_url), output_path+output_file)