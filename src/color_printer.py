# Nuno Lima
import colorama
class ColorPrinter:
    colorama.init(autoreset=True)
    styles = {
        "success":colorama.Fore.GREEN + colorama.Style.BRIGHT,
        "warning":colorama.Fore.YELLOW + colorama.Style.BRIGHT,
        "error":colorama.Fore.RED + colorama.Style.BRIGHT
        }
    @staticmethod
    def show(text: str, type: str = "success", print_end: str = "\n" , on_error_exit = False) -> None:
        message = text
        if type in ColorPrinter.styles:
            message = f'{ColorPrinter.styles[type]}{text}'
        print(message,end=print_end)
        if type == "error" and on_error_exit:
            exit()

    @staticmethod
    def colored(text: str, type: str = "success") -> str:
        message = text
        if type in ColorPrinter.styles:
            message = f'{ColorPrinter.styles[type]}{text}'
        return message
# usage
my_colored_text = ColorPrinter.colored(text="Success") 
ColorPrinter.show(text="Fatal error",type="error",on_error_exit=True)



