from config import Config
from utils.reddit_scraper import reddit_scrapper
from utils.short_maker import short_maker

import random, string, os


def clear_dir(path):
    for file in os.listdir(path):
        os.remove(path+file)


if __name__ == '__main__':
    urls = reddit_scrapper(random.choice(Config.SUBREDDIT_LIST), limit=100)
    filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))+'.mp4'
    short_maker('output/'+filename, urls, resolution=(720, 1280))
    clear_dir('content/videos/')



