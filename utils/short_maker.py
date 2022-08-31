#!/usr/bin/env python3
#-*- coding:utf -8-*-

from moviepy.editor import VideoFileClip, concatenate_videoclips
from .downloader import reddit_downloader, tiktok_downloader, instagram_downloader

import random, string


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


def short_maker(path_out:str, urls:list, resolution:tuple = (720, 1280)):
    vids = []
    duration = 0
    urls_used = []
    
    for url in urls:
        path_vid = 'content/videos/' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        if 'reddit' in url or 'redd.it' in url:
            reddit_downloader(url.replace('\n', ''), path_vid)
        elif 'tiktok' in url:
            tiktok_downloader(url.replace('\n', ''), path_vid)
        elif 'instagram' in url:
            instagram_downloader(url.replace('\n', ''), path_vid)
        
        try:
            video = VideoFileClip(path_vid+'.mp4')
            duration += video.duration
            if duration <= 60:
                urls_used.append(url)
                vids.append(video.resize(width = resolution[0]).set_pos('center'))
            else:
                print(f'\n{y}[ ! ]Some videos could not be included as they exceed 60 seconds of video!{e}\n')
                break
        except: pass
    
    compose = concatenate_videoclips(vids, method='compose').resize(resolution).set_pos('center')
    compose.write_videofile(path_out, fps=30, threads=80, codec="libx264")



