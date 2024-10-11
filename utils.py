import requests
from urllib.parse import urlsplit, unquote
from os.path import split, splitext
from pathlib import Path


def download_pic(url, filename, path):
    Path(f'{path}/').mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(f'{path}/{filename}'), 'wb') as file:
        file.write(response.content)


def get_extension(url):
    sep_url = urlsplit(url)
    path_to_file = split(unquote(sep_url.path))
    path_to_image, image_name = path_to_file
    image = splitext(image_name)
    name, ext = image
    return ext
