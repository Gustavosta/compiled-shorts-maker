#!/usr/bin/env python3
#-*- coding:utf -8-*-

from TikTokAPI import TikTokAPI

from .database import Database
from config import Config
from .utils import instagram_login

import praw, random


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


def instagram_scraper(hashtag:str, limit:int=100):
    post_list = []
    cur = Database()
    duration = 0
    
    try:
        client = instagram_login(Config.SCRAPER_INSTAGRAM_USERNAME, Config.SCRAPER_INSTAGRAM_PASSWORD)
        posts = client.hashtag_medias_v1_chunk(hashtag, max_amount=limit, tab_key='top')
        
        for post in posts[0]:
            if post.video_url is not None:
                if cur.search(id=str(post.id)) == []:
                    if post.video_duration < Config.MAX_DURATION_PER_INSTAGRAM_VIDEO:
                        duration += post.video_duration
                        if duration < 60:
                            post_list.append(str(post.video_url))
                            cur.insert(post.id, str(post.video_url), 'instagram')
        post_list = random.choices(post_list, k=len(post_list))
                            
    except: pass
    
    print(f'\n{y}[ + ]{e} Found {len(post_list)} videos\n')
            
    return post_list


def tiktok_scraper(search:str, limit:int=30):
    cur = Database()
    videos = []
    search = search.replace('#', '').replace(' ', '').strip()
    duration = 0
    
    try:
        api = TikTokAPI()
        content = api.getVideosByHashTag(search, count=limit)['itemList']
        
        for i in random.choices(content, k=len(list(content))):
            print(i['video']['duration'])
            if cur.search(id=i['id']) == []:
                if i['video']['duration'] < Config.MAX_DURATION_PER_TIKTOK_VIDEO:
                    duration += i['video']['duration']
                    if duration < 60:
                        url = f'https://www.tiktok.com/@{i["author"]["uniqueId"]}/video/{i["id"]}'
                        cur.insert(i['id'], url, 'tiktok')
                        videos.append(url)
                    else:
                        break
                    
    except: pass
                
    print(f'\n{y}[ + ]{e} Found {len(videos)} videos\n')
                
    return videos


def reddit_scraper(subreddit:str, limit:int=100):
    cur = Database()
    reddit = praw.Reddit(client_id=Config.SCRAPER_REDDIT_CLIENT_ID, client_secret=Config.SCRAPER_REDDIT_CLIENT_SECRET, user_agent=Config.SCRAPER_REDDIT_USER_AGENT)
    hot_posts = reddit.subreddit(subreddit).hot(limit=limit)
    urls = []
    duration = 0
    
    for post in random.sample(list(hot_posts), limit):
        try:
            media = post.media
            if cur.search(id=str(post.id)) == []:
                if media is not None:
                    if media['reddit_video']['is_gif'] == False and media['reddit_video']['duration'] < Config.MAX_DURATION_PER_REDDIT_VIDEO:
                        duration += media['reddit_video']['duration']
                        if duration <= 60:
                            url = post.media['reddit_video']['fallback_url']
                            cur.insert(post.id, url, 'reddit')
                            urls.append(url)
                        else:
                            break
                    
        except KeyError: pass
    
    print(f'\n{y}[ + ]{e} Found {len(urls)} videos\n')

    return urls


