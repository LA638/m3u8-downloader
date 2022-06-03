#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def save_file(file_name, playlist_url):
    file_list = re.findall('^[^#].+', requests.get(playlist_url).text, flags=re.MULTILINE)
    file_url = re.search('.+\/(?=.+$)', playlist_url)[0]
    file_links = []
    for file in file_list:
        file_links.append(file_url+file)
    try: 
        with open(file_name, 'wb') as file:
            for file_link in tqdm(
            file_links, 
            unit=' files', 
            desc=file_name, 
            miniters=1):
                # if 'seg-1-a1.ts' in file_link:
                #     continue
                file_request = requests.get(file_link, stream=True)
                file.write(file_request.content)
                file.flush()
                sleep(1)
    except (FileExistsError, FileNotFoundError) as error:
        print(error)

def multi_save_file(playlists, threads):
    with ThreadPoolExecutor(threads) as executor:
        executor.map(save_file, playlists.keys(), playlists.values())

def convert_file(file):
    # Ffmpeg video and audio streams to file
    command = f'ffmpeg -hide_banner -loglevel warning -y -i {file[1][0]} -i {file[1][1]} -map 0:V:0 -map 1:a:0 -c copy -f mp4 -movflags +faststart {file[0]}'
    print(command)
    os.popen(command).read()

def multi_convert_file(files, threads):
    with ThreadPoolExecutor(threads) as executor:
        executor.map(convert_file, files)


if __name__ == '__main__':

    save_file('./t32/1080p.ts', 'https://cdn-2.facecast.net/media/csw_69288/AAAAAAAAAAAAAAAAAAAAAPyFOowu7qLqa0i7dVF_4V2GsSTVg0GqlqPUEiJlLaYns3zBVTV0Akj8XxWU4gsOxGhl03q3VLemVDj932JsXiM=.AAAAAAAAAAAAAAAAAAAAALie_MHGmnM7jDRiVDQd-a0wuOqzploTH2OPDrr1PLAaMbbU_qgM3pD5ABrgoLS2YlOaU-trtwcItgtOd8QgbT7B92c37zMtcG8Lf3vhmY71XefOhz_ZKpLfHDgoGWljZ_3h3y1KlQBbj24RuBHHZ6ryiL_huye1VvJWxtZgLP3H9SeHpqugaN2Hxzj_onYHJ9quwH9-uc5aLg7sh54st5Ng-p1nPEah5AcMeGcri3-ORDjOwpKZzJ7jWYHaXdlsmluUes_q9h1-P9a1NQP0D3IpUiTeQIeCs5KL1Gz_5bsT.AZQ3_qLFqvDEfcIzVCB20Q/1080p.m3u8')
    exit()

    urls = {
    './t32/1080p.ts': 'https://cdn-2.facecast.net/media/csw_69288/AAAAAAAAAAAAAAAAAAAAAPyFOowu7qLqa0i7dVF_4V2GsSTVg0GqlqPUEiJlLaYns3zBVTV0Akj8XxWU4gsOxGhl03q3VLemVDj932JsXiM=.AAAAAAAAAAAAAAAAAAAAALie_MHGmnM7jDRiVDQd-a0wuOqzploTH2OPDrr1PLAaMbbU_qgM3pD5ABrgoLS2YlOaU-trtwcItgtOd8QgbT7B92c37zMtcG8Lf3vhmY71XefOhz_ZKpLfHDgoGWljZ_3h3y1KlQBbj24RuBHHZ6ryiL_huye1VvJWxtZgLP3H9SeHpqugaN2Hxzj_onYHJ9quwH9-uc5aLg7sh54st5Ng-p1nPEah5AcMeGcri3-ORDjOwpKZzJ7jWYHaXdlsmluUes_q9h1-P9a1NQP0D3IpUiTeQIeCs5KL1Gz_5bsT.AZQ3_qLFqvDEfcIzVCB20Q/1080p.m3u8',
    # './t16/audio0.aac': 'https://e10-m9.facecast.net/secure/LCD-eoHmt5Am0gTrderE7Q/5mCrXaJFBGm2FcaR8D0xtg/1651509333/18275391/93520/Audio0.m3u8',
    # './t16/source.ts': 'https://e10-m9.facecast.net/secure/LCD-eoHmt5Am0gTrderE7Q/5mCrXaJFBGm2FcaR8D0xtg/1651509333/18275391/93520/source.m3u8',
    # 'audio00.ts': 'https://cs9-21v4.vkuseraudio.net/s/v1/ac/eGB5Fg8soXjkAH7Zb0mYMvuhHUiLtciYs0U1eZ6GcwR8rZ0HzVRGJFzH6o-7m6xsNxNzLThB_OTu597DWx_FU4IhbwtQHC403-na_OPd458Cpe32BeXapcYGtEuCEFnxolFalUPAbIyCaMoGTGJVC64Jcs6pOewTPphHu6lBhAhH18E/index.m3u8',
    # 'audio03.ts': 'https://cs9-3v4.vkuseraudio.net/s/v1/ac/aZpIPES_9oDieajb2PlfC5OfdGgDnkR_FH77NJ8b_0yCVqwaAjeHPfhZR_5Tctl6wtVzMq3OXHNO8OIAcM2aQ6xF4Y50ljM56lCEYWtnZltYIZhJcjfXuMNS_N1N3wPET3wzcDGYc--rCtEeRprIuVg5OuycfQolpCC4AoJkt76KCaw/index.m3u8',
    # 'audio04.ts': 'https://cs9-12v4.vkuseraudio.net/s/v1/ac/d3zJwDFPqYzeN4l0nZ20oreyJKKSCxnOzzTDOx-dtPNFEPZz1wYeW6C_Z04gHGvQyks9PGZTxFTvQGtwyMLjisDlQwBwoQeBqD3fUh3DfEhayCAjlRNacmwHm4xxm50v7qAiQA2DXrlEN79i7T9MDMH89Jr3G5kE1ucQVAVSIC9NcC4/index.m3u8',
    # 'audio05.ts': 'https://cs9-9v4.vkuseraudio.net/s/v1/ac/Jtkqb2buJj7W1vyAkyc1HcnSkOSK8xoAyknfSbgdCbqqlbPqnTYcZJNN1cMrQJSlCdut7nwR7Vc42Q2cb4h4xVbmJXNuVkXPFOtOMv00ywlRF1uBeg6Ss7hyoM4u-Cj4ge1b92p9pRxPrW8UTyRCLAyoNJobtaAMdoFQqJlUOj2mijc/index.m3u8',
    # 'audio06.ts': 'https://cs9-6v4.vkuseraudio.net/s/v1/ac/6wWcCLE99nlRy7jzSrGhWQAYaSQqoByYs7ZzJeaYPBn_Owf4dZ3NQdl_SCtnur9HAdRHbmSR8-357NeVkS5ZBgX9qVNbWgO5Bpu6x7-HgdMfMEKLDsS87F8CnsMnJ6GUtSHwgy21hGkK8OsSlZyp9K975PADPI_qV0BUO5451UJutWU/index.m3u8',
    # 'audio07.ts': 'https://cs9-20v4.vkuseraudio.net/s/v1/ac/MftHbtRbzSRa1mYEzWCRsnCqQBhtvE7aT1npATQ9u8tIwMO5I74GjMZNjXHsj2hdSq3ksa9lUCd0Jd_wbR479S_Fq46kODsdy_Ma6S9ufsyv44R8z3pbpnQQWlUxpwrjjCujIR5rGraBwbQmEQuw1AhtZZwv74okQ_Y94BrXmezBwkA/index.m3u8',
    # 'audio08.ts': 'https://cs9-12v4.vkuseraudio.net/s/v1/ac/tXz6seL-qML1Ia0zbWV21vvFkB1iK6XKwAe21Dm59IxgZT0sZoUrj5NX5b0bMypeiXQgK4fJNpkV-BS6nP3O7lYWqZloyE4zCpWhoweFbdqcJVJiZRvHLY03KR7A48MM1A_kTtMvFP8MY35QC0g2RJSP6K_RT1nSaBj5c0SL2Xu6Hkw/index.m3u8',
    # 'audio09.ts': 'https://cs9-21v4.vkuseraudio.net/s/v1/ac/cfPNFz2oCR9q0OCZPUq9suCDQgq4WUM5U-W7PAZUqOlqXRmbj5bxBYTFnavSCQSnTiXmI2ZkGqDX9cgtTXoR6Jf0HTprSAgy7P3UyuS9aWECKSwz-Bff3iS8zIYjckvzNQfKDtSi8beOjYCbLbAF6REZqmM0OpRgbZws5pIjKPiZ70U/index.m3u8'
    }

    multi_save_file(urls, 4)

    files = [
        ('./t16/source.mp4', ['./t16/source.ts','./t16/audio0.aac']),
        # ('/mnt/c/out/top32_2021E7.mp4', ['/mnt/c/out/top32_video.ts','/mnt/c/out/top32_audio.aac']),
        # ('/mnt/c/out/final_2021E7.mp4', ['/mnt/c/out/final_video.ts','/mnt/c/out/final_audio.aac'])
    ]
    multi_convert_file(files, 4)