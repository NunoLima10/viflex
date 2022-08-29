
import colorama


class LoadBar:
    def __init__(self, Mb_size:float = 100 , length: int = 50, decimals: float  = 1, 
                fill: str = '█', no_fill:str = "-") -> None:

       self.Mb_size =  Mb_size
       self.length = length
       self.decimals = decimals
       self.fill = fill
       self.no_fill = no_fill

       colorama.init(autoreset=True)


    def update(self, Mb_remaining: float) -> None:
        
        Mb_donwloaded = round(self.Mb_size - Mb_remaining,1)
       
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (Mb_donwloaded / self.Mb_size))
        filledLength = int(self.length * Mb_donwloaded // self.Mb_size)

        filled_bar = colorama.Fore.GREEN +  self.fill * filledLength + colorama.Fore.RESET 
        not_filled_bar = self.no_fill * (self.length - filledLength) 

        print(f'\r{Mb_donwloaded}Mb / {self.Mb_size} Mb |{ filled_bar + not_filled_bar}| {percent}%', end = "\r")
        
    
    def finish(self) -> None:
        print("")



