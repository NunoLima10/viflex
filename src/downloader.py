from src.exceptions import NoResolutionDesired
from src.color_printer import ColorPrinter
from src.stream_downloader import StreamDownloader
from src.youtube_link import YouTubeLink
from src.util import regex_search,with_internet

from pytube import YouTube,Playlist

import pathlib
import datetime

class Downloader:
    def __init__(self, args: dict) -> None:
        self.args = args
        self.output_folder = pathlib.Path.cwd()
        ColorPrinter.show(text="Working on it...", type="warning", print_end="\r")
        
    def validate_args(self) -> YouTubeLink:
        
        youtube_link = YouTubeLink(self.args["url"])
        status = youtube_link.available_for_download()

        if not status["available"]:
            ColorPrinter.show(text=status["error_message"], type="error", on_error_exit=True)
        
        if self.args["playlist"] and not youtube_link.is_playlist:
            ColorPrinter.show(text="Provided playlist flag but is a video url", type="error", on_error_exit=True)
        
        self.validate_resolution(self.args["resolution"])
        self.validate_path(self.args["path"])


    def validate_path(self, path: str) -> None:
        if path is not None:
            valid_path = pathlib.Path.is_dir(path)
            if not valid_path:
                ColorPrinter.show(text=f"Provided invalid path {path}", type="error", on_error_exit=True)
            self.output_folder = path

    def validate_resolution(self, resolution: str) -> None:
        if resolution is not None:
            valid_resolution = regex_search(r"^[\d]{3,4}[p]$", resolution)
            if not valid_resolution:
                ColorPrinter.show(text=f"Provided invalid resolution {resolution}",type="error",on_error_exit=True)
    
    def start(self) -> None:
        self.validate_args()
        stream_downloader = StreamDownloader(self.output_folder)

        if self.args["info"]:
            self.complete_info(self.args["url"])
            exit()

        if self.args["thumbnail"]:
            stream_downloader.download_thumbnail(self.args["url"])
    
        if self.args["video"] and not self.args["playlist"]:
            try:
                stream_downloader.download_video(self.args["url"], self.args["resolution"])
            except NoResolutionDesired:
                pass

        if self.args["audio"] and not self.args["playlist"]:
            stream_downloader.download_audio(self.args["url"])

        if self.args["playlist"]:
            stream_downloader.download_play_list(
                url=self.args["url"],
                video_flag=self.args["video"],
                audio_flag=self.args["audio"],
                resolution=self.args["resolution"]
            )

    @with_internet
    def complete_info(self, url: str) -> None:
        youtube_link = YouTubeLink(self.args["url"])

        if youtube_link.is_video:
            self.show_video_info(url)
        
        if youtube_link.is_playlist:
            self.show_playlist_info(url)

    def show_video_info(self, url: str) -> None:
        video = YouTube(url)
        resolutions = self.get_available_resolutions(url)

        duration = str(datetime.timedelta(seconds=video.length))
        label = "Video info".center(20,"=")
        info = f"""{ColorPrinter.colored(text=label,type="warning")}
{ColorPrinter.colored(text="Title:")} {video.title}
{ColorPrinter.colored(text="Channel:")} {video.author}
{ColorPrinter.colored(text="Views:")} {video.views}
{ColorPrinter.colored(text="Duration:")} {duration}
{ColorPrinter.colored(text="Progressive")} {" ".join(resolutions["progressive"])}
{ColorPrinter.colored(text="Adaptive")} {" ".join(resolutions["adaptive"])}
{ColorPrinter.colored(text="Audio")} {" ".join(resolutions["audio"])}
{ColorPrinter.colored(text="="*20,type="warning")}

"""
        print(info)


    def show_playlist_info(self, url: str) -> None:
        playlist = Playlist(url)
        label = "Playlist info".center(20,"=")
        info = f"""{ColorPrinter.colored(text=label,type="warning")}
{ColorPrinter.colored(text="Title:")} {playlist.title}
{ColorPrinter.colored(text="Channel:")} {playlist.owner}
{ColorPrinter.colored(text="Views:")} {playlist.views}
{ColorPrinter.colored(text="Videos:")} {playlist.length}
{ColorPrinter.colored(text="="*20,type="warning")}"""
        print(info)

    @with_internet
    def get_available_resolutions(self, url: str) -> dict:
        video = YouTube(url)
        progressive_streams = video.streams.filter(progressive=True, file_extension='mp4').desc()
        adaptive_streams = video.streams.filter(only_video=True,adaptive=True, file_extension='mp4').desc()
        audio_streams = video.streams.filter(only_audio=True, file_extension='mp4').desc()
        progressive_resolution = [stream.resolution for stream in progressive_streams]
        adaptive_resolution = [stream.resolution for stream in adaptive_streams]
        audio_resolution = [stream.abr for stream in audio_streams]

        return{
            "progressive":list(dict.fromkeys(progressive_resolution)),
            "adaptive":list(dict.fromkeys(adaptive_resolution)),
            "audio":list(dict.fromkeys(audio_resolution))
        }

