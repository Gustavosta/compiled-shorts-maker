#!/usr/bin/env python3
#-*- coding:utf -8-*-

class Config:
    SCHEDULED_POSTING_TIMES = []
    DATABASE_PATH = 'content/database.db'
    
    SCRAPER_REDDIT_CLIENT_ID = ''
    SCRAPER_REDDIT_CLIENT_SECRET = ''
    SCRAPER_REDDIT_USER_AGENT = ''
    SCRAPER_REDDIT_SUBREDDIT_LIST = ['memes']
    MAX_DURATION_PER_REDDIT_VIDEO = 20
    
    SCRAPER_INSTAGRAM_USERNAME = ''
    SCRAPER_INSTAGRAM_PASSWORD = ''
    SCRAPER_INSTAGRAM_HASHTAG_LIST = ['memes']
    MAX_DURATION_PER_INSTAGRAM_VIDEO = 20
    
    SCRAPER_TIKTOK_HASHTAGS = ['memes']
    MAX_DURATION_PER_TIKTOK_VIDEO = 30
    
    GOOGLE_CLIENT_SECRET_PATH = 'client_secret.json'
    
    INSTAGRAM_USERNAME = ''
    INSTAGRAM_PASSWORD = ''

    POST_CATEGORY = 'comedy'
    POST_TITLE = 'Memes I Found #{count} #shorts'
    POST_DESCRIPTION = '#shorts #memes'
    POST_ADDITIONAL_TAGS = []
    POST_LANGUAGE = "en-US"



