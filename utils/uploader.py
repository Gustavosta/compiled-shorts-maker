#!/usr/bin/env python3
#-*- coding:utf -8-*-

from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

from .utils import instagram_login
from config import Config

import os


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


def youtube_uploader(video_path:str, title:str, description:str, category:str, privacy_status:str='public', tags:list=[]):
    channel = Channel()
    credentials_path = 'content/credentials.storage'
    channel.login(Config.GOOGLE_CLIENT_SECRET_PATH , credentials_path)
    if not os.path.exists(video_path):
        print(f"\n{r}[ ! ] Video not found\n{e}")

    elif os.path.isfile(Config.GOOGLE_CLIENT_SECRET_PATH) and os.path.isfile(credentials_path):
        video = LocalVideo(file_path=video_path)

        video.set_title(title)
        video.set_description(description)
        video.set_tags(tags)
        video.set_category(category)
        video.set_default_language(Config.POST_LANGUAGE)
        video.set_embeddable(True)
        video.set_privacy_status(privacy_status)
        video.set_public_stats_viewable(True)
        video = channel.upload_video(video)
        return f'https://www.youtube.com/watch?v={video.id}'
    
    else:
        print(f"\n{r}[ ! ] Client secret and credentials not found\n{e}")


def instagram_uploader(video_path:str, title:str, description:str, tags:list):
    client = instagram_login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)
    formated_tags = []
    
    for tag in tags:
        tag = tag.replace(' ', '').strip()
        if len(formated_tags) <= 25:
            if not '#' in tag:
                formated_tags.append(f'#{tag}')
            else:
                formated_tags.append(tag)

    if os.path.exists(video_path):
        video = client.clip_upload(video_path, title+'\n\n'+description+'\n\n'+' '.join(formated_tags))
        thumbnail_path = video_path+'.jpg'
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            
        return f'https://www.instagram.com/p/{video.code}'

    else:
        print(f"\n{r}[ ! ] Video not found\n{e}")
