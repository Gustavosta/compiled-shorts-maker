#!/usr/bin/env python3
#-*- coding:utf -8-*-

from config import Config
import requests, instagrapi, os


def get_suggest_tags(category:str, platform='youtube'):
    url = f'https://rapidtags.io/api/generator?query={category}&type={platform}'
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['tags']+Config.POST_ADDITIONAL_TAGS
    return []


def instagram_login(username:str, password:str, save_session:bool=True):
    session_path = f"content/instagram_session_{username.lower()}.json"
    client = instagrapi.Client()
    
    if save_session and os.path.exists(session_path):
        client.load_settings(session_path)
    else:
        client.login(username, password)
    
    if save_session and not os.path.exists(session_path):
        client.dump_settings(session_path)
    
    return client

