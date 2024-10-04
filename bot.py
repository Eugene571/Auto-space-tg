import telegram
import os
import time
from dotenv import load_dotenv, find_dotenv
import argparse
from random import shuffle


# Функция для получения случайных изображений
def pics_to_post(directory):
    images = [os.path.join(directory, img) for img in os.listdir(directory) if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    shuffle(images)  # Перемешиваем изображения для случайного выбора
    return images


# Функция для отправки текста в канал
def send_text_to_channel(bot, chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        print(f"Posted text: '{text}' to the channel.")
    except Exception as e:
        print(f"Error posting text: {e}")


def main():
    # Парсер аргументов для указания времени и директории с фото
    parser = argparse.ArgumentParser(
        description='Please enter time interval for posting and directory with pics'
    )
    parser.add_argument('--time', help='time interval between posts in seconds', type=int, default=None)
    parser.add_argument('--path', help='directory consisting pics to post', default='images')
    parser.add_argument('--text', help='text to post in the channel', type=str, default=None)
    args = parser.parse_args()

    # Загрузка переменных окружения
    load_dotenv(find_dotenv())
    bot = telegram.Bot(token=os.getenv('TG_API_KEY'))
    chat_id = os.getenv('TG_CHAT_ID')

    # Получаем частоту публикаций из флага --time или переменной окружения POST_FREQ
    post_freq = args.time if args.time is not None else int(os.getenv('POST_FREQ', 14400))  # Приоритет флага --time

    # Если нужно отправить текст
    if args.text:
        send_text_to_channel(bot, chat_id, args.text)

    # Получаем список изображений
    images = pics_to_post(args.path)

    while True:
        # Публикуем изображения одно за другим
        for image in images:
            try:
                # Отправляем фото в указанный чат
                with open(image, 'rb') as img:
                    bot.send_photo(chat_id=chat_id, photo=img)
                print(f"Posted {image} to the channel.")

                # Ждем заданный интервал времени перед публикацией следующего фото
                time.sleep(post_freq)
            except Exception as e:
                print(f"Error posting {image}: {e}")

        # Перемешиваем изображения снова для рандомного порядка
        shuffle(images)


if __name__ == '__main__':
    main()

