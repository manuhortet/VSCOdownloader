import json
import re
import requests
import urllib
from bs4 import BeautifulSoup


def download_picture(url):
    if not is_valid_url(url):
        import pdb
        pdb.set_trace()
        return None, None

    if is_mobile_url(url):
        url = get_public_url(url)

    response = requests.get(url)
    if response.status_code is 404:
        pdb.set_trace()
        return None, None

    picture_id = url.rsplit('/', 1)[-1]
    return get_picture_and_author(response.text, picture_id)


def is_mobile_url(url):
    decomposed_url = url.rsplit('/')
    if len(decomposed_url) == 4 and decomposed_url[2] == 'vs.co':
        return True
    return False


def is_valid_url(url):
    decomposed_url = url.rsplit('/')
    if len(decomposed_url) >= 4 and decomposed_url[2] in ['vsco.co', 'vs.co']:
        return True
    return False


def get_public_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    raw_link = soup.find("meta", property="al:ios:url")["content"].rsplit('?', 1)[0]

    author = raw_link.rsplit('/')[3]
    id = raw_link.rsplit('/')[5]

    return f'https://vsco.co/{author}/media/{id}'


def get_picture_and_author(html, pic_id):
    preload_state = re.findall('window.__PRELOADED_STATE__ = (.*?)</script>', html)[0]
    picture_data = json.loads(preload_state).get("medias").get("byId").get(pic_id).get('media')

    author = picture_data.get('gridName')
    file_url = "https://" + picture_data.get('responsiveUrl')

    return file_url, author
