#!/usr/bin/env python3
#-*- coding:utf -8-*-

from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from config import Config

import os, logging


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


def youtube_uploader(video_path, title, description, category, privacy_status, tags):
    channel = Channel()
    credentials_path = 'content/credentials.storage'
    channel.login(Config.GOOGLE_CLIENT_SECRET_PATH , credentials_path)
    if not os.path.exists(video_path):
        logging.error(f"\n{r}[ ! ] Video not found\n{e}")

    elif os.path.isfile(Config.GOOGLE_CLIENT_SECRET_PATH) and os.path.isfile(credentials_path):
        video = LocalVideo(file_path=video_path)

        video.set_title(title)
        video.set_description(description)
        video.set_tags(tags)
        video.set_category(category)
        video.set_default_language(Config.YOUTUBE_LANGUAGE)
        video.set_embeddable(True)
        video.set_privacy_status(privacy_status)
        video.set_public_stats_viewable(True)
        video = channel.upload_video(video)
        return video.id
    else:
        logging.error(f"\n{r}[ ! ] Client secret and credentials not found\n{e}")


