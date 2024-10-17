import colorama
from colorama import Fore, Back, Style
colorama.init()
def question(*arg, end='\n', sep=' ')->None:
    """ Prints in blue color """
    print(Fore.BLUE + sep.join(arg) + Style.RESET_ALL, end=end)

def warning(*arg, end='\n', sep=' ')->None:
    """ Prints in light red color """
    print(Back.LIGHTRED_EX + sep.join(arg) + Style.RESET_ALL, end=end)


def title(*arg, end='\n', sep=' ', decorator=None)->None:
    """ Prints in bright green color with a title format """
    if decorator is not None:
        print(decorator*10 + Fore.LIGHTGREEN_EX + sep.join(arg) + Style.RESET_ALL + decorator*10, end=end)
    else:
        print(Fore.LIGHTGREEN_EX + sep.join(arg) + Style.RESET_ALL, end=end)

def _(*arg, end='\n', sep=' ')->None:
    """ Prints in white color """
    print(Fore.WHITE + sep.join(arg) + Style.RESET_ALL, end=end)

def inp(message:str='')->str:
    return input(Fore.YELLOW +"[Press Enter to continue]>| "+ Style.RESET_ALL+message)


if __name__ == "__main__":
    warning("waring")
    question("qprint")
    title("tprint")
    _("title")