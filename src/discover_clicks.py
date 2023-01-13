from os import walk, path
from log import Log
from pydub import AudioSegment


def discover_clicks(p: str):
    Log.printinfo(f"Discovering clicks in {p}")
    player1_exists = False
    player2_exists = False

    for _, dirs, _ in walk(p):
        for d in dirs:
            if d == "player1":
                Log.printinfo("Found /player1")
                player1_exists = True
                p1c, p1r, p1sc, p1sr, p1hc, p1hr = search_player(path.join(p, "player1"), 1)
            elif d == "player2":
                Log.printinfo("Found /player2")
                player2_exists = True
                p2c, p2r, p2sc, p2sr, p2hc, p2hr = search_player(path.join(p, "player2"), 2)

    if not player1_exists:
        Log.printerr("/player1 directory doesn't exist! Please follow the clickpack format.")
        return
    if not player2_exists:
        Log.printinfo("/player2 directory doesn't exist! Using /player1's clicks for player 2.")
        p2c, p2r, p2sc, p2sr, p2hc, p2hr = p1c, p1r, p1sc, p1sr, p1hc, p1hr

    return p1c, p2c, p1r, p2r, p1sc, p2sc, p1sr, p2sr, p1hc, p2hc, p1hr, p2hr


def search_player(p: str, player: int):
    clicks = list()
    releases = list()
    softclicks = list()
    softreleases = list()
    hardclicks = list()
    hardreleases = list()

    clicks_exists = False
    releases_exists = False
    softclicks_exists = False
    softreleases_exists = False
    hardclicks_exists = False
    hardreleases_exists = False

    Log.printinfo(f"Searching {p}")
    for _, dirs, _ in walk(p):
        for d in dirs:
            if d not in ("clicks", "releases", "softclicks", "softreleases", "hardclicks", "hardreleases"):
                continue
            for root, _, files in walk(path.join(p, d)):
                for f in files:
                    if f.endswith(".wav"):
                        if d == "clicks":
                            clicks.append(load_correct_format(root, f))
                            clicks_exists = True
                        elif d == "releases":
                            releases.append(load_correct_format(root, f))
                            releases_exists = True
                        elif d == "softclicks":
                            softclicks.append(load_correct_format(root, f))
                            softclicks_exists = True
                        elif d == "softreleases":
                            softreleases.append(load_correct_format(root, f))
                            softreleases_exists = True
                        elif d == "hardclicks":
                            hardclicks.append(load_correct_format(root, f))
                            hardclicks_exists = True
                        elif d == "hardreleases":
                            hardreleases.append(load_correct_format(root, f))
                            hardreleases_exists = True

    if not clicks_exists and player == 1:
        Log.printerr("/player1 has no clicks! Please follow the clickpack format.")
    if not releases_exists:
        Log.printinfo(f"No releases found for player {player}, using silence.")
        releases.append(AudioSegment.silent(duration=0))
    if not softclicks_exists:
        Log.printinfo(f"No softclicks found for player {player}, using regular clicks.")
        softclicks = clicks
    if not softreleases_exists:
        Log.printinfo(f"No softreleases found for player {player}, using regular releases.")
        softreleases = releases
    if not hardclicks_exists:
        Log.printinfo(f"No hardclicks found for player {player}, using regular clicks.")
        hardclicks = clicks
    if not hardreleases_exists:
        Log.printinfo(f"No hardreleases found for player {player}, using regular releases.")
        hardreleases = releases

    return clicks, releases, softclicks, softreleases, hardclicks, hardreleases

def load_correct_format(root, f):
    if f.endswith(".wav"):
        return AudioSegment.from_wav(path.join(root, f))
    elif f.endswith(".mp3"):
        return AudioSegment.from_mp3(path.join(root, f))
    elif f.endswith(".ogg"):
        return AudioSegment.from_ogg(path.join(root, f))