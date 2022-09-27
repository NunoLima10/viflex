from src.color_printer import ColorPrinter
from src.exceptions import NoResolutionDesired
from src.load_bar import LoadBar
from src.youtube_link import YouTubeLink
from src.util import with_internet,download_image

from pytube import YouTube,Playlist

import datetime
import pathlib

load_bar = LoadBar()

class StreamDownloader:
    def __init__(self, output_folder: str) -> None:
        self.output_folder = output_folder
        self.video_prefix = "Viflex-v-"
        self.audio_prefix = "Viflex-a-"
    
    def on_progress(stream, chunk, file_handle, bytes_remaining):
        load_bar.update(bytes_remaining)
        
    def on_complete(chunk, file_handle, bytes_remaining):
        load_bar.finish() 
        ColorPrinter.show(text="Downloaded successfully")    
    
    @with_internet
    def download_thumbnail(self, url: str) -> None:
        youtube_link = YouTubeLink(url)

        if youtube_link.is_playlist and not youtube_link.is_video:
            return 
        
        ColorPrinter.show(text="Downloading thumbnail")

        video = YouTube(url)
        download_image(
            url =video.thumbnail_url,
            name=video.title,
            output_folder=self.output_folder,
        )

    def download_audio(self, url: str) -> None:
        video = YouTube(
            url,
            on_progress_callback=self.on_progress,
            on_complete_callback=self.on_complete
        )

        self.show_short_info(video)

        ColorPrinter.show(text="Finding audio stream", print_end="\r")
        stream = video.streams.filter(only_audio=True, file_extension='mp4').desc().first()
        
        ColorPrinter.show(text="CTRL + C to cancel   ", type="warning")

        load_bar.total_size = stream.filesize
        load_bar.update(stream.filesize)
        file = stream.download(
            output_path=self.output_folder,
            filename_prefix=self.audio_prefix
        )
        path = pathlib.Path(file)
        try:
            path.rename(path.with_suffix('.mp3'))
        except FileExistsError:
            ColorPrinter.show(text="File already exists", type="warning")
            path.unlink()

    @with_internet
    def download_video(self, url: str, resolution: str = None): 
        video = YouTube(
            url,
            on_progress_callback=self.on_progress,
            on_complete_callback=self.on_complete
        )

        self.show_short_info(video)

        ColorPrinter.show(text="Finding videos stream", print_end="\r")
        stream = video.streams.get_highest_resolution()

        ColorPrinter.show(text="CTRL + C to cancel   ", type="warning")
        progressive = True

        if resolution is not None:
            progressive = False
            stream = self.get_by_resolution(video.streams, resolution)

        load_bar.total_size = stream.filesize
        load_bar.update(stream.filesize)
        stream.download(
            output_path=self.output_folder,
            filename_prefix=self.video_prefix
        )
        if not progressive:
            self.download_audio(url)
            
    @with_internet
    def download_play_list(self, url: str, video_flag: bool, audio_flag: bool, thumbnail_flag: bool, 
                            resolution: str) -> None:

        playlist = Playlist(url)

        for video in playlist.videos:
            youtube_link = YouTubeLink(video.watch_url)
            status = youtube_link.available_for_download()

            if not status["available"]:
                ColorPrinter.show(text=status["error_message"], type="error")
                ColorPrinter.show(text="Video skipped", type="warning")
                continue

            if video_flag or (not video_flag and not audio_flag and not thumbnail_flag):
                try:
                    self.download_video(video.watch_url, resolution)
                except NoResolutionDesired:
                    ColorPrinter.show(text="Video does not have the selected resolution", type="error")
                    ColorPrinter.show(text="Video skipped", type="warning")
            
            if audio_flag:
                self.download_audio(video.watch_url)
            
            if thumbnail_flag:
                self.download_thumbnail(video.watch_url)

    def get_by_resolution(self, streams: YouTube.streams, resolution: str):
        streams = streams.filter(only_video=True,adaptive=True,file_extension='mp4').desc()
        for stream in streams:
            if stream.resolution == resolution:
                return stream
        raise NoResolutionDesired
    
    def show_short_info(self, video: YouTube) -> None:
        duration = str(datetime.timedelta(seconds=video.length))
        label = "Video info".center(20,"=")
        info = f"""{ColorPrinter.colored(text=label, type="warning")}
{ColorPrinter.colored(text="Title:")} {video.title}
{ColorPrinter.colored(text="Channel:")} {video.author}
{ColorPrinter.colored(text="Duration:")} {duration}
{ColorPrinter.colored(text="="*20,type="warning")}"""
        print(info)
