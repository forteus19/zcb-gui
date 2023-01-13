class Colors:
    reset = '\033[0m'
    fg = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }

    bg = {
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m'
    }


class Log:
    @staticmethod
    def printwarn(text):
        print(
            f'[{Colors.fg["yellow"]}!{Colors.reset}]{Colors.fg["yellow"]} WARNING: {Colors.reset}{text}{Colors.reset}')

    @staticmethod
    def printerr(text):
        print(f'[{Colors.fg["red"]}-{Colors.reset}]{Colors.fg["red"]} ERROR: {Colors.reset}{text}{Colors.reset}')

    @staticmethod
    def printinfo(text):
        print(f'[{Colors.fg["blue"]}i{Colors.reset}]{Colors.fg["blue"]} INFO: {Colors.reset}{text}{Colors.reset}')

    @staticmethod
    def printsuccess(text):
        print(f'[{Colors.fg["green"]}+{Colors.reset}]{Colors.fg["green"]} SUCCESS: {Colors.reset}{text}{Colors.reset}')
