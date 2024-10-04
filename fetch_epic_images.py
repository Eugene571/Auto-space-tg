import requests
import os
import datetime
import argparse
from dotenv import load_dotenv, find_dotenv
from utils import download_pic


def create_pic_info_list(payload):
    pic_info_url = f'https://api.nasa.gov/EPIC/api/natural/available'
    response = requests.get(pic_info_url, params=payload)
    response.raise_for_status()
    pic_info = response.json()
    return pic_info


def fetch_epic_pic(payload, pic, pic_number, path):
    needed_date = datetime.date.fromisoformat(pic)
    formated_date = needed_date.strftime('%Y/%m/%d')
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{needed_date}'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pic_url_for_download = f'https://api.nasa.gov/EPIC/archive/natural/{formated_date}/png/' \
                           f'{response.json()[0]["image"]}.png'
    filename = f'nasa_EPIC_{pic_number}.png'
    response = requests.get(pic_url_for_download, params=payload)
    try:
        response.raise_for_status()
        download_pic(response.url, filename, path)
    except IndexError:
        print('there is no photo on EPIC for the requested date:', formated_date)


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='saves photo from NASA Epic'
    )
    parser.add_argument('number_of_pic', type=int, help='number of pictures to save')
    parser.add_argument('--path', help='saving directory', default='images')
    args = parser.parse_args()
    nasa_api_key = os.environ['NASA_API_KEY']

    payload = {'api_key': nasa_api_key}
    pic_info = create_pic_info_list(payload)
    for index, pic in enumerate(pic_info[(-int(args.number_of_pic) - 1):-1], start=1):
        try:
            fetch_epic_pic(payload, pic, index, args.path)
            print(f'saved picture #{index}')
        except ValueError:
            print('please type integer')


if __name__ == '__main__':
    main()
