from os import listdir, path, walk
from pydub import AudioSegment

from log import log

def discover_clicks(folder: str):
    '''Processes a clickpack.
    '''

    p1_click_folders = list()
    p2_click_folders = list()

    
    player_dirs = listdir(folder)
    log.printinfo(f'Player directories: {player_dirs}')

    '''
    Now, for player_dir (player1, player2) we will have to process click folders
    (clicks, releases, softclicks, softreleases)
    '''
    for player_dir in player_dirs:
        log.printinfo(f'Observing Path: {path.join(folder, player_dir)}')
        log.printinfo(f'Current Player Directory: {player_dir}')

        for _, dirnames, _ in walk(path.join(folder, player_dir)):
            for dirname in dirnames:
                if player_dir == 'player1':
                    p1_click_folders.append(path.join(folder, player_dir, dirname))
                elif player_dir == 'player2':
                    p2_click_folders.append(path.join(folder, player_dir, dirname))

            
    log.printsuccess(f'Finished discovering click folders! Now processing Media.')

    p1_clicks = list()
    p1_releases = list()
    p1_softclicks = list()
    p1_softreleases = list()
    p1_hardclicks = list()
    p1_hardreleases = list()
    
    p2_clicks = list()
    p2_releases = list()
    p2_softclicks = list()
    p2_softreleases = list()
    p2_hardclicks = list()
    p2_hardreleases = list()

    log.printinfo(f'Player 1 clicks finished!')
    for folder in p1_click_folders:
        log.printinfo(f'Current Directory: {folder}')
        for (_, _, filenames) in walk(folder):
            log.printinfo(f'This folder contains: {filenames}')
            current_click_type = folder.split('\\')[-1]

            log.printinfo(f'Current Folder Type: {current_click_type}')
            log.printinfo(f'Current Player: Player 1')
            
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): 
                    log.printinfo(f'Adding File: {file}')
                    full_paths.append(path.join(folder, file))
                    
                else:
                    log.printwarn(f'File is not a wav file! Skipping: {file}')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            
            for click_path in full_paths:
                try: 

                    
                    if current_click_type == 'clicks':
                        log.printsuccess(f'Finished Processing! ({click_path})')
                        p1_clicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'releases':
                        p1_releases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softclicks':
                        p1_softclicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softreleases':
                        p1_softreleases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'hardclicks':
                        p1_hardclicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'hardreleases':
                        p1_hardreleases.append(AudioSegment.from_wav(click_path))
                
                except:
                    if click_path.endswith('.wav'): 

                        log.printerr(f'Failed to process "{click_path}", perhaps it\'s corrupted?')
                    else:
                        if not click_path.endswith('.txt'): 
                            log.printwarn(f'Failed to process "{click_path}", perhaps it\'s not a .wav?')
    
    log.printinfo(f'Processing Player 2 clicks.')
    for folder in p2_click_folders:
        log.printinfo(f'Current Directory: {folder}')
        for (_, _, filenames) in walk(folder):
            log.printinfo(f'This folder contains: {filenames}')
            current_click_type = folder.split('\\')[-1]

            log.printinfo(f'Current Folder Type: {current_click_type}')
            log.printinfo(f'Current Player: Player 2')

            
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): 
                    log.printinfo(f'Adding File: {file}')
                    full_paths.append(path.join(folder, file))
                    
                else:
                    log.printwarn(f'File is not a wav file! Skipping: {file}')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            
            for click_path in full_paths:
                try: 

                    
                    if current_click_type == 'clicks':
                        log.printsuccess(f'Finished Processing! ({click_path})')
                        p2_clicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'releases':
                        p2_releases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softclicks':
                        p2_softclicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softreleases':
                        p2_softreleases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'hardclicks':
                        p2_hardclicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'hardreleases':
                        p2_hardreleases.append(AudioSegment.from_wav(click_path))
                
                except:
                    if click_path.endswith('.wav'): 

                        log.printerr(f'Failed to process "{click_path}", perhaps it\'s corrupted?')
                    else:
                        if not click_path.endswith('.txt'): 
                            log.printerr(f'Failed to process "{click_path}", perhaps it\'s not a .wav?')

    log.printinfo(f'Checking Info...\n')

    if p1_clicks == []:
        log.printerr(f'Player 1 has no clicks! Please follow the click format.')
    if p2_clicks == []: 
        log.printwarn('Player 2 has no clicks! Using Player 1 clicks.')
        p2_clicks = p1_clicks

    if p1_releases == []:
        log.printwarn('Player 1 has no releases! Using nothing.')
        p1_releases.append(AudioSegment.silent(duration=0))
    if p2_releases == []:
        log.printwarn('Player 2 has no releases! Using Player 1 releases.')
        p2_releases = p1_releases

    if p1_softclicks == []:
        log.printwarn('Player 1 has no softclicks! Using Player 1 clicks.')
        p1_softclicks = p1_clicks
    if p2_softclicks == []:
        log.printwarn('Player 2 has no softclicks! Using Player 2 clicks.')
        p2_softclicks = p2_clicks
    
    if p1_softreleases == []:
        log.printwarn('Player 1 has no softreleases! Using Player 1 releases.')
        p1_softreleases = p1_releases
    if p2_softreleases == []:
        log.printwarn('Player 2 has no softreleases! Using Player 2 releases.')
        p2_softreleases = p2_releases
    
    if p1_hardclicks == []:
        log.printwarn('Player 1 has no hardclicks! Using Player 1 clicks.')
        p1_hardclicks = p1_clicks
    if p2_hardclicks == []:
        log.printwarn('Player 2 has no hardclicks! Using Player 2 clicks.')
        p2_hardclicks = p2_clicks
    
    if p1_hardreleases == []:
        log.printwarn('Player 1 has no hardreleases! Using Player 1 releases.')
        p1_hardreleases = p1_releases
    if p2_hardreleases == []:
        log.printwarn('Player 2 has no hardreleases! Using Player 2 releases.')
        p2_hardreleases = p2_releases
    
    log.printsuccess(f'Complete! Please check the log for any errors.')

    '''Variables explanation
    
    p1_clicks = list()
    p2_clicks = list()
    p1_releases = list()
    p2_releases = list()
    p1_hardclicks = list()
    p2_hardclicks = list()

    p1_softclicks = list()
    p2_softclicks = list()
    p1_softreleases = list()
    p2_softreleases = list()
    p1_hardreleases = list()
    p2_hardreleases = list()

    Those can return an empty list if the folder does not exist:

    [0] - p1 clicks
    [1] - p2 clicks
    [2] - p1 releases
    [3] - p2 releases
    [4] - p1 softclicks
    [5] - p2 softclicks
    [6] - p1 softreleases
    [7] - p2 softreleases
    [8] - p1 hardclicks
    [9] - p2 hardclicks
    [10] - p1 hardreleases
    [11] - p2 hardreleases
    '''

    return (
        p1_clicks,
        p2_clicks,
        p1_releases,
        p2_releases,
        p1_softclicks,
        p2_softclicks,
        p1_softreleases,
        p2_softreleases,
        p1_hardclicks,
        p2_hardclicks,
        p1_hardreleases,
        p2_hardreleases
    )