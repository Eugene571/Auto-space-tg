import requests
from dotenv import load_dotenv, find_dotenv
import argparse
from utils import download_pic


def fetch_spacex_last_launch(launch_id, path):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    photos_to_save = response.json()['links']['flickr']['original']
    if photos_to_save:
        for index, pic in enumerate(photos_to_save, start=1):
            filename = f'spacex_launch{index}.jpg'
            download_pic(pic, filename, path)
            print(f'Saved {filename}')
    else:
        print('No available photos for this launch')


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='saves photos from SpaceX rocket launch'
    )
    parser.add_argument('--launch_id', help='launch id', default='latest')
    parser.add_argument('--path', help='saving directory', default='images')
    args = parser.parse_args()
    fetch_spacex_last_launch(args.launch_id, args.path)


if __name__ == '__main__':
    main()
