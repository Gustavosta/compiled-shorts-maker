#!/usr/bin/env python3
#-*- coding:utf -8-*-

import requests
from config import Config


def get_suggest_tags(category, platform='youtube'):
    url = f'https://rapidtags.io/api/generator?query={category}&type={platform}'
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['tags']+Config.ADDITIONAL_TAGS
    return []

