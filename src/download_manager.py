from src.youtube_link import YouTubeLink
from src.color_printer import ColorPrinter
from src.load_bar import LoadBar
from src.util import regex_search
from pytube import YouTube

import pathlib
import datetime

load_bar = LoadBar()
printer =  ColorPrinter()

class DownloadManager:
    def __init__(self, args: dict) -> None:
        self.args = args
        self.file_path = pathlib.Path.cwd()
        printer.show("Working on it...","warning",print_end="\r")
        self.validate_args() 
    
    def validate_args(self) -> None:
        youtube_link = YouTubeLink(self.args["url"])
        status = youtube_link.available_for_download()

        if not status["available"]:
            printer.show(status["error_message"],"error")
            exit()
        
        if self.args["playlist"] and not youtube_link.is_playlist:
            printer.show("Provided playlist flag but is a video url","error")
            exit()
        
        self.validate_quality(self.args["quality"])
        self.validate_path(self.args["path"])
        

    def validate_path(self, path: str) -> bool:
        if path is not None:
            valid_path = pathlib.Path.exists(path)
            if not valid_path:
                printer.show(f"Provided invalid path {path}","error")
                exit()


    def validate_quality(self, quality: str) -> bool:
        if quality is not None:
            valid_quality = regex_search(r"^[\d]{3,4}[p]$", quality)
            if not valid_quality:
                printer.show(f"Provided invalid quality {quality}","error")
                exit()



    # def start(self) -> None:
    #     if not self.video_info:
    #         return
    #     self.video_info.register_on_progress_callback(self.on_progress)
    #     self.video_info.register_on_complete_callback(self.on_complete)
        
    #     if self.video:
    #         self.download_video()
    #     if self.audio:
    #         self.download_audio()
    #     if not self.video and not self.audio:
    #         self.download_video()

    # def download_video(self) -> None: 
    #     stream = self.video_info.streams.get_highest_resolution()
    #     load_bar.total_size = stream.filesize
    #     load_bar.update(stream.filesize)
    #     stream.download(output_path=self.file_path,filename_prefix="Viflex-v-")  

    # def download_audio(self) -> None:
    #     stream =  self.video_info.streams.filter(only_audio=True).first()
    #     load_bar.total_size = stream.filesize
    #     load_bar.update(stream.filesize)
    #     file = stream.download(output_path=self.file_path,filename_prefix="Viflex-a-")
    #     path = pathlib.Path(file)
    #     path.rename(path.with_suffix('.mp3'))
        
    # def on_progress(stream, chunk, file_handle, bytes_remaining):
    #     load_bar.update(bytes_remaining)
        
    # def on_complete(chunk, file_handle, bytes_remaining):
    #     load_bar.finish() 
    #     printer.show("Downloaded successfully")

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