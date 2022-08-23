from .database import Database
from config import Config
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

import praw, random, requests, os


def reddit_scrapper(subreddit, limit=100):
    cur = Database()
    reddit = praw.Reddit(client_id=Config.REDDIT_CLIENT_ID, client_secret=Config.REDDIT_CLIENT_SECRET, user_agent=Config.REDDIT_USER_AGENT)
    hot_posts = reddit.subreddit(subreddit).hot(limit=limit)
    urls = []
    duration = 0
    for post in random.sample(list(hot_posts), limit):
        try:
            media = post.media
            if cur.search(id=str(post.id)) == []:
                if media is not None:
                    if media['reddit_video']['is_gif'] == False and media['reddit_video']['duration'] < 20:
                        duration += media['reddit_video']['duration']
                        if duration <= 60:
                            url = post.media['reddit_video']['fallback_url']
                            cur.insert(post.id, url)
                            urls.append(url)
                        else:
                            break
                    
        except KeyError: pass

    return urls


def download_file(url, path):
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


def download_reddit(url, path):
    download_file(url, path+'_temp.mp4')
    download_file(url.split('DASH')[0]+'DASH_audio.mp4', path+'.mp3')
    # Unir audio e vídeo no moviepy
    audio = AudioFileClip(path+'.mp3')
    video = VideoFileClip(path+'_temp.mp4')
    if audio:
        compose = concatenate_videoclips([video.set_audio(audio)])
        compose.write_videofile(path+'.mp4', fps=30, codec="libx264")
        os.remove(path+'_temp.mp4')
        os.remove(path+'.mp3')
    else:
        compose = concatenate_videoclips([video])
        compose.write_videofile(path+'.mp4', fps=30, codec="libx264")
        os.remove(path+'_temp.mp4')

    return path+'.mp4'
    



