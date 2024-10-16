import requests
import os
import argparse
from dotenv import load_dotenv, find_dotenv
from utils import download_pic, get_extension


def create_apod_pic_list(payload):
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    apod_pics = response.json()
    return apod_pics


def fetch_apod_pics(apod_pics, path):
    pics_url = []
    for pic in apod_pics:
        if pic['url']:
            try:
                pics_url.append(pic['thumbnail_url'])
            except KeyError:
                pics_url.append(pic['url'])
        else:
            print(pic['date'], 'no photo for this date')

    for index, pic in enumerate(pics_url):
        file_ext = get_extension(pic)
        filename = f'nasa_apod_{index}{file_ext}'
        download_pic(pic, filename, path)


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='saves photo from NASA APOD'
    )
    parser.add_argument('number_of_pic', type=int, help='number of pictures to save')
    parser.add_argument('--path', help='saving directory', default='images')
    args = parser.parse_args()
    nasa_api_key = os.environ['NASA_API_KEY']
    payload = {'api_key': nasa_api_key,
               'count': args.number_of_pic,
               'thumbs': True
               }
    apod_pics = create_apod_pic_list(payload)
    try:
        fetch_apod_pics(apod_pics, args.path)
        print('pictures saved')
    except ValueError:
        print('please type integer')


if __name__ == '__main__':
    main()
