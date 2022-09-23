from src.argparser import ArgParser
from src.downloader import Downloader

__author__ = "Nuno Lima"
__copyright__ = "Copyright 2022 Nuno Lima"
__version__ = "0.2.0"
__maintainer__ = "Nuno Lima"
__email__ = "contato.playcraft@gmail.com"
__status__ = "Production"

def main() -> None:
    arg_parser = ArgParser()
    args = arg_parser.parse()
    download_manager = Downloader(args)
    download_manager.start()

if __name__=="__main__":
    main()