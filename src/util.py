from urllib.request import urlopen
from urllib.error import URLError
import re

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
