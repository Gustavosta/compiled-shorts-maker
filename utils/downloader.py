#!/usr/bin/env python3
#-*- coding:utf -8-*-

from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

import requests, urllib.parse, os, time


def download_file(url:str, path:str):
    try:
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return True
    
    except:
        return False


def tiktok_downloader(url:str, path:str):
    r = requests.get('https://tiktok-dl.id/info?url='+urllib.parse.quote(url))
    if r.status_code == 200:
        return download_file(r.json()['aweme_detail']['video']['play_addr']['url_list'][0], path)


def reddit_downloader(url:str, path:str):
    download_file(url, path+'_temp.mp4')
    download_file(url.split('DASH')[0]+'DASH_audio.mp4', path+'.mp3')
    
    try:
        video = VideoFileClip(path+'_temp.mp4')
        audio = AudioFileClip(path+'.mp3')
        compose = concatenate_videoclips([video.set_audio(audio)])
        compose.write_videofile(path+'.mp4', fps=30, codec="libx264")
    except:
        video = VideoFileClip(path+'_temp.mp4')
        compose = concatenate_videoclips([video])
        compose.write_videofile(path+'.mp4', fps=30, codec="libx264")
        
    time.sleep(1)
    os.remove(path+'_temp.mp4')
    os.remove(path+'.mp3')
        
    return path


def instagram_downloader(url:str, path:str):
    return download_file(url, path)



