from src.color_printer import ColorPrinter
from src.load_bar import LoadBar
from pytube import YouTube,exceptions

import pathlib
import argparse
import datetime

load_bar = LoadBar()
printer =  ColorPrinter()


class DownloadManager:
    def __init__(self, args: argparse.Namespace) -> None:
        self.video = args.v
        self.audio = args.a
        self.video_info = None
        try:
            self.video_info = YouTube(args.url)
        except exceptions.RegexMatchError:
            printer.show(f'Provided an invalid url {args.url}',"error")
        except exceptions.VideoUnavailable:
            printer.show("Private videos cannot be downloaded","warning")

        self.file_path = pathlib.Path.cwd()
       
            
    def start(self) -> None:
        if not self.video_info:
            return

        self.video_info.register_on_progress_callback(self.on_progress)
        self.video_info.register_on_complete_callback(self.on_complete)
        
        self.show_video_info()

        if self.video:
            self.donwload_video()
           

        if self.audio:
            self.donwload_audio()
           

        if not self.video and not self.audio:
            self.donwload_video()

    def donwload_video(self) -> None: 
        stream = self.video_info.streams.get_highest_resolution()
        self.Mb_size = round((stream.filesize/1024)/1024,1)
        load_bar.Mb_size = self.Mb_size
        load_bar.update(self.Mb_size)
        stream.download(output_path = self.file_path)
   
    def donwload_audio(self) -> None:
        stream =  self.video_info.streams.filter(only_audio=True).first()
        self.Mb_size = round((stream.filesize/1024)/1024,1)
        load_bar.Mb_size = self.Mb_size
        load_bar.update(self.Mb_size)
        file = stream.download(output_path = self.file_path)
        path = pathlib.Path(file)
        path.rename(path.with_suffix('.mp3'))
        
    def on_progress(stream, chunk, file_handle,bytes_remaining):
        Mb_remaining =  round((bytes_remaining/1024)/1024,1)
        load_bar.update(Mb_remaining)
        
    def on_complete(chunk, file_handle,bytes_remaining):
        load_bar.finish() 
        printer.show("Downloaded successfully")

    def show_video_info(self) -> None:
        duration = str(datetime.timedelta(seconds=self.video_info.length))

        printer.show("=== Video info ===","warning")

        printer.show('Title: ',print_end="")
        print(self.video_info.title)

        printer.show('Channel: ',print_end="")
        print(self.video_info.author)

        printer.show('Duration: ',print_end="")
        print(f'{duration} mim')

        printer.show("==================","warning")
      

        