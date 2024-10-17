import colorama
from colorama import Fore, Back, Style
import time
colorama.init()

class BasePrinter:
    """ Clase base para impresiones con animación """

    def __init__(self) -> None:
        self._time_to_write = 0.005
    
    def print_with_animation(self, message: str, color: str, end='\n', flush=True):
        """ Imprime el mensaje con un efecto de escritura """
        for char in message:
            print(color + char, end='', flush=flush)  # Imprimir cada carácter
            time.sleep(self._time_to_write)  # Pausa para crear el efecto de escritura
        print(Style.RESET_ALL, end=end)  # Restablecer el estilo al final

class Printer(BasePrinter):
    """ Clase para impresiones específicas """

    def question(self, *arg, end='\n', sep=' ')->None:
        """ Prints in blue color with typing animation """
        message = sep.join(arg)
        self.print_with_animation(message, Fore.BLUE, end)

    def warning(self, *arg, end='\n', sep=' ')->None:
        """ Prints in light red color with typing animation """
        message = sep.join(arg)
        self.print_with_animation(message, Back.LIGHTRED_EX, end)

    def title(self, *arg, end='\n', sep=' ', decorator=None)->None:
        """ Prints in bright green color with a title format and typing animation """
        message = sep.join(arg)
        if decorator is not None:
            print(decorator*10 + Fore.LIGHTGREEN_EX, end='')  # Imprimir decorador
            self.print_with_animation(message, Fore.LIGHTGREEN_EX, end="" if decorator is not None else end)
            print(Style.RESET_ALL + decorator*10, end=end)  # Restablecer el estilo al final
        else:
            self.print_with_animation(message, Fore.LIGHTGREEN_EX, end)

    def _(self, *arg, end='\n', sep=' ')->None:
        """ Prints in white color with typing animation """
        message = sep.join(arg)
        self.print_with_animation(message, Fore.WHITE, end)

    def inp(self,message:str='',custom_color:str=None)->str:
        final_message = ((custom_color + message + Style.RESET_ALL) if custom_color is not None else message)
        return input(Fore.YELLOW + "[Press Enter to continue]>| "+Style.RESET_ALL+final_message)
printer  = Printer()
# Uso de la clase Printer
if __name__ == "__main__":
    
    printer.warning("waring")
    printer.question("qprint")
    printer.title("tprint")
    printer._("title")
