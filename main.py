from src.download_manager import DownloadManager
import argparse

__author__ = "Nuno Lima"
__copyright__ = "Copyright 2022 Nuno Lima"
__version__ = "0.1.0"
__maintainer__ = "Nuno Lima"
__email__ = "contato.playcraft@gmail.com"
__status__ = "Production"

def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","-video",help="download only the video",action="store_true")
    parser.add_argument("-a","-audio",help="download only the audio",action="store_true")
    parser.add_argument("url",help="video url must be in quotes",type=str)
    
    return parser.parse_args()


def main() -> None:
    args =  arg_parser()
    download_manager = DownloadManager(args)
    download_manager.start()

if __name__=="__main__":
    main()