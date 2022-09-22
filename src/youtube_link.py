from src.exceptions import VideoUnavailable,PlaylistUnavailable,InvalidURL
from src.util import regex_search

from pytube import extract,request,Playlist
class YouTubeLink:
    def __init__(self, url: str) -> None:
        self.url = url
        self._is_video: bool = None
        self._is_playlist: bool = None
        self.video_url_pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        self.playlist_url_pattern = r"(?:list=)([0-9A-Za-z_-]{11}).*"

    def check_video_availability(self):
        video_id = extract.video_id(self.url)
        watch_url = f"https://youtube.com/watch?v={video_id}"
        watch_html = request.get(url=watch_url)

        status, messages = extract.playability_status(watch_html)
        if status == 'UNPLAYABLE':
            raise VideoUnavailable

    def check_playlist_availability(self) -> None:
        if not Playlist(self.url).videos:
            raise PlaylistUnavailable

    @property
    def is_video(self) -> bool:
        if self._is_video:
            return self._is_video
        self._is_video = regex_search(self.video_url_pattern, self.url)
        return self._is_video

    @property
    def is_playlist(self) -> bool:
        if self._is_playlist:
            return self._is_playlist
        self._is_playlist = regex_search(self.playlist_url_pattern, self.url)
        return self._is_playlist

    def test_url(self) -> None:
        if not(self.is_video or self.is_playlist):
            raise InvalidURL
        
        if self.is_video:
            self.check_video_availability()
        
        if self.is_video and self.is_playlist:
            self.check_playlist_availability()

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
        except PlaylistUnavailable:
            available_flag = False
            error_message = "Playlist is unavailable"
        
        return {"available": available_flag,"error_message": error_message}


