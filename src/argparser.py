import argparse
import pathlib

class ArgParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Download videos and music from You Tube through your terminal",
            prog="viflex",
            epilog="%(prog)s 0.2.0",
        )

        self.parser.add_argument("-v", "--video",help="download only the video",action="store_true")
        self.parser.add_argument("-a", "--audio",help="download only the audio",action="store_true")
        self.parser.add_argument("-t", "--thumbnail",help="download only the thumbnail",action="store_true")
        self.parser.add_argument("-pl", "--playlist",help="download all videos from playlist",action="store_true")
        self.parser.add_argument("-i", "--info",help="show detailed information about video or playlist",action="store_true")
        self.parser.add_argument("-r", "--resolution",help="select video resolution")
        self.parser.add_argument("--version", action='version', version='%(prog)s 0.2.0')
        self.parser.add_argument('-p','--path', type=pathlib.Path,help="select output folder")
        self.parser.add_argument("url", help="video url must be in quotes",type=str)

    def parse(self) -> None:
        self.arg =  self.parser.parse_args()
        return vars(self.arg)

