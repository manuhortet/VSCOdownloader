import json
import re
import requests
import urllib


def download_picture(url):
    id, filename = get_picture_data(url)

    response = requests.get(url)
    if response.status_code is 404:
        return None

    picture_url = get_picture(response.text, id)

    return picture_url


def get_picture_data(url):
    picture_id = url.rsplit('/', 1)[-1]
    filename = f"{picture_id}.png"
    return picture_id, filename


def get_picture(html, id):
    preload_state = re.findall('window.__PRELOADED_STATE__ = (.*?)</script>', html)[0]
    picture_data = json.loads(preload_state).get("medias").get("byId")
    file_url = "https://" + str(picture_data.get(id).get('media').get('responsiveUrl'))

    return file_url
