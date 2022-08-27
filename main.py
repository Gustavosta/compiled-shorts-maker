#!/usr/bin/env python3
#-*- coding:utf -8-*-

from config import Config
from utils.reddit_scraper import reddit_scrapper
from utils.short_maker import short_maker
from utils.youtube_uploader import youtube_uploader
from utils.utils import *

from datetime import datetime

import random, string, os, schedule


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


def clear_dir(path):
    for file in os.listdir(path):
        os.remove(path+file)


def create_dirs(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def post_shorts():
    create_dirs(['content/', 'content/videos/', 'output/'])
    
    # Utility variables
    date = datetime.now().strftime('%m/%d/%Y')
    count = len(os.listdir('output'))+1
    
    print(f'\n{y}[ + ] Creating short...{e}\n')
    urls = []
    for subreddit in random.choices(Config.SUBREDDIT_LIST, k=len(Config.SUBREDDIT_LIST)):
        urls = reddit_scrapper(subreddit, limit=500)
        if len(urls) > 2:
            break
        
    if not len(urls) == 0:
        platform = 'youtube'
        filename = 'shorts_'+''.join(random.choices(string.ascii_lowercase + string.digits, k=5))+'.mp4'
        short_maker('output/'+filename, urls, resolution=(720, 1280))
        tags = get_suggest_tags(Config.YOUTUBE_CATEGORY, platform)
        id = youtube_uploader('output/'+filename, Config.YOUTUBE_TITLE.format(**locals()), Config.YOUTUBE_TITLE.format(**locals()), Config.YOUTUBE_CATEGORY, 'public', tags)
        clear_dir('content/videos/')
        print(f'\n{y}[ + ] Short created and uploaded:{e} http://youtu.be/{id}\n')

    else:
        print(f'\n{r}[ ! ] No posts were found on Reddit{e}\n')


if __name__ == '__main__':
    post_shorts()



