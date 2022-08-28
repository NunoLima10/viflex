
from color_printer import ColorPrinter

import argparse

def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","-video",help="Download format",action="store_true")
    parser.add_argument("-m","-music",help="Download format",action="store_true")
    parser.add_argument("link",help="Video link",type=str)
    
    return parser.parse_args()


def main() -> None:
   args =  arg_parser()
  
if __name__=="__main__":
    main()