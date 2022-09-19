from crypt import methods
from src.youtube_link import YouTubeLink
from src.color_printer import ColorPrinter
from src.load_bar import LoadBar
from src.util import regex_search
from pytube import YouTube,Playlist

import pathlib
import datetime

load_bar = LoadBar()


class DownloadManager:
    def __init__(self, args: dict) -> None:
        self.args = args
        self.file_path = pathlib.Path.cwd()
        self.video_prefix = "Viflex-v-"
        self.audio_prefix = "Viflex-a-"
        ColorPrinter.show("Working on it...","warning",print_end="\r")
        
    
    def validate_args(self) -> YouTubeLink:
        youtube_link = YouTubeLink(self.args["url"])
        status = youtube_link.available_for_download()

        if not status["available"]:
            ColorPrinter.show(status["error_message"],"error",on_error_exit=True)
        
        if self.args["playlist"] and not youtube_link.is_playlist:
            ColorPrinter.show("Provided playlist flag but is a video url","error",on_error_exit=True)
        
        self.validate_quality(self.args["quality"])
        self.validate_path(self.args["path"])


    def validate_path(self, path: str) -> None:
        if path is not None:
            valid_path = pathlib.Path.exists(path)
            if not valid_path:
                ColorPrinter.show(f"Provided invalid path {path}","error",on_error_exit=True)
        self.file_path = path

    def validate_quality(self, quality: str) -> None:
        if quality is not None:
            valid_quality = regex_search(r"^[\d]{3,4}[p]$", quality)
            if not valid_quality:
                ColorPrinter.show(f"Provided invalid quality {quality}","error",on_error_exit=True)

    def start(self) -> None:
        if self.args["info"]:
            self.complete_info(self.args["url"])
            exit()
        
        # if self.args["thumbnail"]:
        #     self.download_thumbnail()
        
        # if self.args["playlist"]:
        #     self.download_playlist()
        
        # if self.args["video"]:
        #     self.download_video()

        # if self.args["audio"]:
        #     self.download_audio()

        # if not self.video and not self.audio:
        #     self.download_video()

    def complete_info(self, url: str) -> None:
        youtube_link = YouTubeLink(self.args["url"])
        status = youtube_link.available_for_download()

        if not status["available"]:
            return
        
        if youtube_link.is_video:
            self.show_video_info(url)
        
        if youtube_link.is_playlist:
            self.show_playlist_info(url)

    def show_video_info(self, url: str) -> None:
        video = YouTube(url)
        duration = str(datetime.timedelta(seconds=video.length))

        info = f"Title: {video.title}\nChannel: {video.author}\nViews: {video.views}\nDuration: {duration} mim"
        
        ColorPrinter.show("Video info".center(20,"="),"warning")
        print(info)
        ColorPrinter.show("="*30,"warning")


    def show_playlist_info(self, url: str) -> None:
        playlist = Playlist(url)
        try:
            info = f"Title: {playlist.title}\nChannel: {playlist.owner}\nViews: {playlist.views}\nVideos: {playlist.length}"
        except KeyError:
            info = "Playlist have no info"

        ColorPrinter.show("Playlist info".center(20,"="),"warning")
        print(info)
        ColorPrinter.show("="*30,"warning")

        # def download_video(self) -> None: 
    #     video = YouTube(self.args["url"])
    #     stream = video.streams.get_highest_resolution()
    #     progressive = True

    #     if self.args["quality"] is not None:
    #         stream = self.get_by_resolution(video.streams, self.args["quality"])
    #         progressive = False
        
    #     if stream is None:
    #         printer.show(f"The video does not have the desired quality","error")
    #         exit()
        
    #     if not progressive:
    #         self.download_audio()
        
    #     video.register_on_progress_callback(self.on_progress)
    #     video.register_on_complete_callback(self.on_complete)
        
    #     load_bar.total_size = stream.filesize
    #     load_bar.update(stream.filesize)
    #     stream.download(
    #         output_path=self.file_path,
    #         filename_prefix=self.video_prefix
    #     )  

    # def download_audio(self) -> None:
    #     video = YouTube(self.args["url"])
    #     stream = video.streams.filter(only_audio=True, file_extension='mp4').desc().first()

    #     load_bar.total_size = stream.filesize
    #     load_bar.update(stream.filesize)

    #     file = stream.download(
    #         output_path=self.file_path,
    #         filename_prefix=self.audio_prefix
    #     )
    #     path = pathlib.Path(file)
    #     path.rename(path.with_suffix('.mp3'))
        
    # def download_thumbnail(self) -> None:
    #     pass

    # def show_video_info(self) -> None:
    #     duration = str(datetime.timedelta(seconds=self.video_info.length))

    #     printer.show("=== Video info ===","warning")

    #     printer.show('Title: ',print_end="")
    #     print(self.video_info.title)

    #     printer.show('Channel: ',print_end="")
    #     print(self.video_info.author)

    #     printer.show('Duration: ',print_end="")
    #     print(f'{duration} mim')

    #     printer.show("==================","warning")
    #     printer.show("(CRTL + C) To cancel","warning")

    # def complete_info(self) -> None:
    #     pass

    #     pass

    # def download_playlist(self) -> None:
    #     pass
    # def get_available_qualities(self, url: str) -> dict:
    #     video = YouTube(url)
    #     progressive_streams = video.streams.filter(progressive=True, file_extension='mp4').desc()
    #     adaptive_streams = video.streams.filter(only_video=True,adaptive=True, file_extension='mp4').desc()
    #     audio_streams = video.streams.filter(only_audio=True, file_extension='mp4').desc()
    #     progressive_qualities = [stream.resolution for stream in progressive_streams]
    #     adaptive_qualities = [stream.resolution for stream in adaptive_streams]
    #     audio_qualities = [stream.abr for stream in audio_streams]

    #     return{
    #         "progressive":list(dict.fromkeys(progressive_qualities)),
    #         "adaptive":list(dict.fromkeys(adaptive_qualities)),
    #         "audio":list(dict.fromkeys(audio_qualities))
    #     }
    
    # def get_by_resolution(self, streams:YouTube.streams, resolution):
    #     streams.filter(only_video=True,adaptive=True, file_extension='mp4').desc()
    #     for stream in streams:
    #         if stream.resolution == resolution:
    #             return stream
    #     return None


    # def on_progress(stream, chunk, file_handle, bytes_remaining):
    #     load_bar.update(bytes_remaining)
        
    # def on_complete(chunk, file_handle, bytes_remaining):
    #     load_bar.finish() 
    #     printer.show("Downloaded successfully")    