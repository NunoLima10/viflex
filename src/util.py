import requests
from urllib.request import urlopen
from urllib.error import URLError
import re
import pathlib
from pytube import YouTube

def regex_search(pattern: str, string: str) -> bool:
    regex = re.compile(pattern)
    results = regex.search(string)
    return results is not None


def is_internet() -> bool:
    try:
        urlopen("https://www.google.com/", timeout=1)
        return True
    except URLError:
        return False

def download_image(url: str, name: str, output_folder: str) -> None:
    img_data = requests.get(url).content
    file = f"{output_folder}/{name}.jpg"
    with open(file, 'wb') as handler:
        handler.write(img_data)
