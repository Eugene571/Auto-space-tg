# NASA & SpaceX Image Fetcher and Telegram Bot

This project consists of Python scripts for downloading images from NASA's APOD, NASA's EPIC, and SpaceX's API, and a Telegram bot to automatically post those images to a channel.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [fetch_apod_images.py](#fetch_apod_imagespy)
  - [fetch_epic_images.py](#fetch_epic_imagespy)
  - [fetch_spacex_images.py](#fetch_spacex_imagespy)
  - [bot.py](#botpy)
- [Utilities](#utilities)
- [License](#license)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Eugene571/Auto-space-tg.git
   cd Auto-space-tg
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Create a .env file in the project root and fill in the following environment variables:
## Environment Variables   
   | Variable       | Description                                      |
| -------------- | ------------------------------------------------ |
| `NASA_API_KEY` | Your NASA API key for fetching images.            |
| `TG_API_KEY`   | Your Telegram bot API key.                        |
| `TG_CHAT_ID`   | Your Telegram channel chat ID (e.g., `@channel`). |
| `POST_FREQ`    | Time interval between posts (in seconds).         |

Example `.env` file: 
```bash 
NASA_API_KEY='your_nasa_api_key'
TG_API_KEY='your_telegram_api_key'
TG_CHAT_ID='@your_channel_id'
POST_FREQ='14400'
```

## Usage
### fetch_apod_images.py
Fetches images from NASA's Astronomy Picture of the Day (APOD) API.
### Example command: 
```bash 
python fetch_apod_images.py 5 --path images
```

- `5` is the number of images to fetch
- `--path` is the directory where images will be saved (default: `images`)

### fetch_epic_images.py
Fetches images from NASA's EPIC (Earth Polychromatic Imaging Camera) API.
### Example command: 

```bash 
python fetch_epic_images.py 5 --path images
```

- `5` is the number of images to fetch
- `--path` is the directory where images will be saved (default: `images`)

### fetch_spacex_images.py
Fetches images from SpaceX's last rocket launch using the SpaceX API.
### Example command:

```bash 
python fetch_spacex_images.py --launch_id latest --path images
```

- `--launch_id` specifies the ID of the launch (default: `latest`).
- `--path` is the directory where images will be saved (default: `images`)

### bot.py
Posts the images to a Telegram channel at regular intervals.
### Example command:

```bash
python bot.py --time 3600 --path images
```

- `--time` is the time interval between posts (default: `POST_FREQ` environment variable).
- `--path` specifies the directory with images to post (default: `images`).

Post a certain photo: 
```bash
python bot.py --image NASA_PIC.jpg
```
- `--image` specifies a file name to be posted, file extension required.

  
## Utilities
- `utils.py` includes helper functions like:
  - `download_pic(url, filename, path)` for downloading pictures.
  - `get_extention(url)` for getting the file extension from a URL.

## License
This project is licensed under the MIT License.
