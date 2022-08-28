
from color_printer import ColorPrinter

def main() -> None:
    printer =  ColorPrinter()

    printer.show("text")
    printer.show("success","success")
    printer.show("warning","warning")
    printer.show("error","error")

if __name__=="__main__":
    main()