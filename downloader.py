#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def make_directory(directory_name):
    try:
        os.mkdir(directory_name)
    except (FileExistsError, FileNotFoundError) as error:
        print(error)

def get_playlist(playlist_url, output_path):
    out_file = output_path+playlist_url[0]
    file_list = re.findall('^[^#].+', requests.get(playlist_url[1]).text, flags=re.MULTILINE)
    file_url = re.search('.+\/(?=.+$)', playlist_url[1])[0]
    file_links = []
    for file in file_list:
        file_links.append(file_url+file)
    return out_file, file_links

def save_file(playlist):
    try: 
        with open(playlist[0], 'wb') as file:
            for file_link in tqdm(
            playlist[1], 
            unit=' files', 
            desc=playlist[0], 
            miniters=1,
            colour='#ee1a80'):
                file_request = requests.get(file_link, stream=True)
                file.write(file_request.content)
                file.flush()
    except (FileExistsError, FileNotFoundError) as error:
        print(error)

def multi_save_file(playlists):
    with ThreadPoolExecutor(6) as executor:
        executor.map(save_file, playlists)

def convert_file(file):
    # Ffmpeg video and audio streams to file
    command = f'ffmpeg -hide_banner -loglevel warning -y -i {file[1][0]} -i {file[1][1]} -map 0:V:0 -map 1:a:0 -c copy -f mp4 -movflags +faststart {file[0]}'
    print(command)
    os.popen(command).read()

def multi_convert_file(files):
    with ThreadPoolExecutor(3) as executor:
        executor.map(convert_file, files)


if __name__ == '__main__':
    output_path = '/mnt/c/out/'
    make_directory(output_path)

    urls = {
    'qual_video.ts':'https://cdn-2.facecast.net/public/69363/720p.m3u8',
    'qual_audio.aac':'https://cdn-2.facecast.net/public/69363/Audio0.m3u8',

    'top32_video.ts':'https://e10-fd.facecast.net/secure/cH2zJKGPnNRwsPollGxCSg/tv4aNB96BOpFyQ4Or3lLRw/1632909804/11006638/69393/720p.m3u8',
    'top32_audio.aac':'https://e10-fd.facecast.net/secure/cH2zJKGPnNRwsPollGxCSg/tv4aNB96BOpFyQ4Or3lLRw/1632909804/11006638/69393/Audio0.m3u8',
    
    'final_video.ts':'https://cdn-1.facecast.net/secure/-GivtdLk5kEwjUVA_pHR4w/tv4aNB96BOpFyQ4Or3lLRw/1632909874/11006642/69364/720p.m3u8',
    'final_audio.aac':'https://cdn-1.facecast.net/secure/-GivtdLk5kEwjUVA_pHR4w/tv4aNB96BOpFyQ4Or3lLRw/1632909874/11006642/69364/Audio0.m3u8'
    }
    playlists = [get_playlist(url, output_path) for url in urls.items()]
    multi_save_file(playlists)

    files = [
        ('/mnt/c/out/qual_2021E6.mp4', ['/mnt/c/out/qual_video.ts','/mnt/c/out/qual_audio.aac']),
        ('/mnt/c/out/top32_2021E6.mp4', ['/mnt/c/out/top32_video.ts','/mnt/c/out/top32_audio.aac']),
        ('/mnt/c/out/final_2021E6.mp4', ['/mnt/c/out/final_video.ts','/mnt/c/out/final_audio.aac'])
    ]
    multi_convert_file(files)