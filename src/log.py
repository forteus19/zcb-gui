class colors:
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

class log:
    def printwarn(text):
        print(f'[{colors.fg["yellow"]}!{colors.reset}]{colors.fg["yellow"]} WARNING: {colors.reset}{text}{colors.reset}')
    def printerr(text):
        print(f'[{colors.fg["red"]}-{colors.reset}]{colors.fg["red"]} ERROR: {colors.reset}{text}{colors.reset}')
    def printinfo(text):
        print(f'[{colors.fg["blue"]}i{colors.reset}]{colors.fg["blue"]} INFO: {colors.reset}{text}{colors.reset}')
    def printsuccess(text):
        print(f'[{colors.fg["green"]}+{colors.reset}]{colors.fg["green"]} SUCCESS: {colors.reset}{text}{colors.reset}')