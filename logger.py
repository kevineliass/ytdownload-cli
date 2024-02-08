from colorama import init, Fore
from sys import stdout, stderr

class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose
        init(autoreset=True)
    
    def set_verbose(self, verbose):
        self.verbose = verbose
    
    def print(self, message='', end='\n', file=stdout):
        if self.verbose:
            print(message, end=end, file=file)
    
    def input(self, message=''):
        i = input(f'{message} ')
        return i

    def log(self, message='', end='\n', file=stdout):
        if self.verbose:
            print(f'[+] {message}', end=end, file=file)
    
    def warn(self, message='', end='\n', file=stdout):
        if self.verbose:
            print(Fore.YELLOW + f'[!] {message}' + Fore.RESET, end=end, file=file)
    
    def err(self, message='', end='\n', file=stderr):
        print(Fore.RED + f'[-] {message}' + Fore.RESET, end=end, file=file)
    
    def debug(self, message='', end='\n', file=stdout):
        print(Fore.BLUE + f'[DEBUG] {message}' + Fore.RESET, end=end, file=file)

console = Logger()