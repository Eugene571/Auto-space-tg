import requests
import os
import datetime
import argparse
from dotenv import load_dotenv, find_dotenv
from utils import download_pic


def create_pic_info_list(payload):
    pic_info_url = 'https://api.nasa.gov/EPIC/api/natural/available'
    response = requests.get(pic_info_url, params=payload)
    response.raise_for_status()
    return response.json()


def fetch_epic_pics(payload, pic, pic_number, path):
    needed_date = datetime.date.fromisoformat(pic)
    pic_download_url = get_epic_pic_url(needed_date, payload)
    if pic_download_url:
        download_and_save_pic(pic_download_url, pic_number, path, payload['api_key'])
    else:
        print('There is no photo on EPIC for the requested date:', needed_date)


def get_epic_pic_url(needed_date, payload):
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{needed_date}'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pic_info = response.json()

    if not pic_info:  # если pic_info пустой, выбрасываем исключение
        raise ValueError(f'No image found for date: {needed_date}')

    pic_name = pic_info[0]["image"]
    return f'https://api.nasa.gov/EPIC/archive/natural/{needed_date.strftime("%Y/%m/%d")}/png/{pic_name}.png'


def download_and_save_pic(pic_url, pic_number, path, api_key):
    filename = f'nasa_EPIC_{pic_number}.png'
    pic_url_with_key = f"{pic_url}?api_key={api_key}"
    response = requests.get(pic_url_with_key)
    print(f'Trying to download from: {pic_url_with_key}')
    print(f'Status code: {response.status_code}')

    response.raise_for_status()  # исключение будет выброшено здесь, если статус не 200
    download_pic(response.url, filename, path)


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(description='saves photo from NASA Epic')
    parser.add_argument('number_of_pic', type=int, help='number of pictures to save')
    parser.add_argument('--path', help='saving directory', default='images')
    args = parser.parse_args()
    payload = {'api_key': os.environ['NASA_API_KEY']}

    try:
        pic_info = create_pic_info_list(payload)
        for index, pic in enumerate(pic_info[-args.number_of_pic:], start=1):
            fetch_epic_pics(payload, pic, index, args.path)
            print(f'Saved picture #{index}')
    except ValueError as ve:
        print(ve)
    except requests.HTTPError as he:
        print(f'HTTP error occurred: {he}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    main()
