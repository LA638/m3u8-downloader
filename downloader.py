#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


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


def save_file(file_links, out_path, out_file):
    try: 
        os.remove(out_path+out_file)
    except (FileExistsError, FileNotFoundError) as error:
        print(error)
    for file_link in file_links:
        with open(out_path+out_file, 'ab') as file:
            file_request = requests.get(file_link, stream=True)
            print(f'{file_link} {file_request}  {len(file_request.content)//1024} kB  {file.tell()//(1024**2)} MB')
            # for chunk in file_request.iter_content(chunk_size=1024):
            #     file.write(chunk)
            file.write(file_request.content)
    

if __name__ == '__main__':
    # Load environment variables from .env file to memory
    load_dotenv()
    print(os.getenv('PLAYLIST_URL'), os.getenv('OUTPUT_PATH'), os.getenv('OUTPUT_FILENAME'))

    # Make output directory
    make_directory(os.getenv('OUTPUT_PATH'))

    playlist = get_playlist(os.getenv('PLAYLIST_URL'))
    save_file(playlist, os.getenv('OUTPUT_PATH'), os.getenv('OUTPUT_FILENAME'))