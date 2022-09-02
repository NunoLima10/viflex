
from hurry.filesize import alternative
from hurry.filesize import size
import colorama

class LoadBar:
    def __init__(self, total_size: float = 100 , length: int = 50, decimals: float = 1, 
                fill: str = '█', no_fill:str = "-") -> None:

       self.total_size =  total_size
       self.length = length
       self.decimals = decimals
       self.fill = fill
       self.no_fill = no_fill

       colorama.init(autoreset=True)

    def clear_line(self) -> None:
        print(" " * 100,end="\r")

    def update(self, remaining: int) -> None:
        
        finished = self.total_size - remaining
       
        percent = round(100 * finished / self.total_size, self.decimals)
        filledLength = int(self.length * finished // self.total_size)

        filled_bar = colorama.Fore.GREEN +  self.fill * filledLength + colorama.Fore.RESET 
        not_filled_bar = self.no_fill * (self.length - filledLength) 

        finished_label =  size(finished,system=alternative)
        total_size_label =  size(self.total_size,system=alternative)
        self.clear_line()
        print(f'\r{finished_label} / {total_size_label} |{ filled_bar + not_filled_bar}| {percent} %', end = "\r")
        
    def finish(self) -> None:
        print("")



