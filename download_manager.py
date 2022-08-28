
import pathlib
from color_printer import ColorPrinter
from pytube import YouTube

import argparse

class DownloadManager:
    def __init__(self, args: argparse.Namespace) -> None:
        self.video = args.v
        self.audio = args.a
        self.link  = args.link
        self.file_path = pathlib.Path.cwd()
        
        self.printer =  ColorPrinter()

    def donwload(self) -> None:
        if self.video:
            self.donwload_video()

        if self.audio:
            self.donwload_audio()

        if not self.video and not self.audio:
            self.donwload_video()
        

          
    def donwload_video(self) -> None:
        video = YouTube(self.link)
        stream =  video.streams.get_highest_resolution()
        stream.download()
        self.printer.show("Video baixado com sucesso")
        
    def donwload_audio(self) -> None:
        video = YouTube(self.link)
        stream =  video.streams.filter(only_audio=True).first()
        file = stream.download()
        path = pathlib.Path(file)
        path.rename(path.with_suffix('.mp3'))
        self.printer.show("Audio baixado com sucesso")
        