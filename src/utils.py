import sys
import os.path
import requests
from tkinter.messagebox import askyesno
import webbrowser

from log import Log

CURRENT_VERSION = 4

# changed to be compatible with pyinstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_for_updates():
    Log.printinfo("Checking for updates...")
    url = "https://forteus19.github.io/latest/zcb-gui.json"
    try:
        d = requests.get(url).json()
    except:
        Log.printerr("Failed to check for updates! Skipping...")
        return
    if d["version"] > CURRENT_VERSION:
        Log.printinfo("An update is available!")
        redirect = askyesno("Update Available", "A new version of zcb-gui is available. Do you want to be redirected to the download page?")
        if redirect:
           webbrowser.open("https://github.com/forteus19/zcb-gui/releases/latest")
           sys.exit(0)
    else:
        Log.printinfo("You're up to date!")