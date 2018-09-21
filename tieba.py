# coding: utf-8
import requests
import config

API = 'http://tieba.baidushabi.com/api/post'

last_tid = 123


def get_update_post():
    global last_tid
    params = {
        'pageIndex': 1,
        'pageSize': 10
    }
    r = requests.post(API, json=params)
    posts = r.json()['data']['data']
    authors = [post['author'] for post in posts]
    updated_posts = []
    for author in config.TIEBA_AUTHORS:
        if author in authors and int(posts[authors.index(author)]['tid']) > last_tid:
            updated_posts.append(posts[authors.index(author)])

    last_tid = max(int(post['tid']) for post in posts)

    return updated_posts
