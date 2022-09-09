
import colorama

class ColorPrinter:
    def __init__(self) -> None:
        colorama.init(autoreset=True)

        self.styles = {
            "success":colorama.Fore.GREEN + colorama.Style.BRIGHT,
            "warning":colorama.Fore.YELLOW + colorama.Style.BRIGHT,
            "error":colorama.Fore.RED + colorama.Style.BRIGHT
        }

    def show(self, text: str, type: str = "success", print_end: str = "\n") -> None:
        message = text
        if type in self.styles:
            message = f'{self.styles[type]}{text}'
        print(message,end=print_end)


