import telegram
import os
import time
from dotenv import load_dotenv, find_dotenv
import argparse
from random import choice
from telegram.error import TelegramError, NetworkError


def post_pics(directory):
    return [os.path.join(directory, img) for img in os.listdir(directory) if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]


def try_to_send_photo(bot, chat_id, photo_path):
    try:
        with open(photo_path, 'rb') as img:
            bot.send_photo(chat_id=chat_id, photo=img)
        print(f"Posted {photo_path} to the channel.")
    except (FileNotFoundError, TelegramError) as e:
        print(f"Error posting {photo_path}: {e}")


def try_to_send_text(bot, chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        print(f"Posted text: '{text}' to the channel.")
    except TelegramError as e:
        print(f"Error posting text: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Please enter time interval for posting, directory with pics, and optionally specify a single image'
    )
    parser.add_argument('--time', help='time interval between posts in seconds', type=int, default=None)
    parser.add_argument('--path', help='directory consisting pics to post', default='images')
    parser.add_argument('--image', help='specific image to post', type=str, default=None)
    parser.add_argument('--text', help='text to post in the channel', type=str, default=None)
    args = parser.parse_args()

    load_dotenv(find_dotenv())
    bot = telegram.Bot(token=os.environ['TG_API_KEY'])
    chat_id = os.environ['TG_CHAT_ID']

    post_freq = args.time if args.time is not None else int(os.getenv('POST_FREQ', 14400))

    if args.text:
        try_to_send_text(bot, chat_id, args.text)

    images = post_pics(args.path)

    if args.image:
        image_path = args.image if os.path.isabs(args.image) else os.path.join(args.path, args.image)
        if os.path.exists(image_path):
            try_to_send_photo(bot, chat_id, image_path)
        else:
            print(f"Image {image_path} does not exist.")
        return

    posted_images = set()
    while True:
        available_images = [img for img in images if img not in posted_images]

        if not available_images:
            print('All available photos have been posted.')
            break

        image = choice(available_images)

        while True:
            try:
                try_to_send_photo(bot, chat_id, image)
                posted_images.add(image)
                break
            except (NetworkError, TelegramError) as e:
                print(f"Network error occurred: {e}. Retrying in 5 seconds...")
                time.sleep(5)

        time.sleep(post_freq)


if __name__ == '__main__':
    main()
