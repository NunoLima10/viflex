from pytube import extract,request
from src.util import regex_search

class InvalidURL(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class VideoUnavailable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class YouTubeLink:
    def __init__(self, url: str) -> None:
        self.url = url
        self.video_url_pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        self.playlist_url_pattern = r"(?:list=)([0-9A-Za-z_-]{11}).*"

    def check_video_availability(self):

        video_id = extract.video_id(self.url)
        watch_url = f"https://youtube.com/watch?v={video_id}"
        watch_html = request.get(url=watch_url)

        status, messages = extract.playability_status(watch_html)

        for reason in messages:
            if status == 'UNPLAYABLE':
                if reason == (
                    'Join this channel to get access to members-only content '
                    'like this video, and other exclusive perks.'
                ):
                    raise VideoUnavailable
                elif reason == 'This live stream recording is not available.':
                    raise VideoUnavailable
                else:
                    raise VideoUnavailable
            elif status == 'LOGIN_REQUIRED':
                if reason == (
                    'This is a private video. '
                    'Please sign in to verify that you may see it.'
                ):
                    raise VideoUnavailable
            elif status == 'ERROR':
                if reason == 'Video unavailable':
                    raise VideoUnavailable
            elif status == 'LIVE_STREAM':
                raise VideoUnavailable

    def test_url(self) -> None:
        self.is_video = regex_search(self.video_url_pattern,self.url)
        self.is_playlist = regex_search(self.playlist_url_pattern,self.url)

        if not(self.is_video or self.is_playlist):
            raise InvalidURL
        
        if self.is_video:
            self.check_video_availability()

    def available_for_download(self) -> dict:
        available_flag = True
        error_message = ""
        try: 
            self.test_url()
        except InvalidURL:
            available_flag = False
            error_message = f'Provided an invalid url "{self.url}"'
        except VideoUnavailable:
            available_flag = False
            error_message = "Video is unavailable for download, possible reasons(MembersOnly,Private)"
        
        return {"available": available_flag,"error_message": error_message}

# urls = {
#     "private_video":"https://www.youtube.com/watch?v=Ki_Szad3hNE", 
#     "private_playlist":"https://www.youtube.com/playlist?list=PLLcS6ldQh_lwGNK3Nx-aDikadwYLLyFM9",
#     "invalid_url":"link", 
#     "playlist_url":"https://www.youtube.com/playlist?list=PLLcS6ldQh_lwxzNRjsAgwjVg_CcOJsxFd",
#     "short":"https://www.youtube.com/shorts/89pR3PQsxpg",
#     "video_on_playlist":"https://www.youtube.com/watch?v=BiQIc7fG9pA&list=RDGMEM6ijAnFTG9nX1G-kbWBUCJAVMJnzVOgNR_rE&index=27"
# }

# for name,url in urls.items():
#     print("\n\n")
#     link = YouTubeLink(url)
#     label = f"{name} {link.available_for_download()} \nis video {link.is_video} is playlist {link.is_playlist} "
#     print(label)


