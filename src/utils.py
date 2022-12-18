import random, sys
from pydub import AudioSegment
from tqdm import tqdm
from os import path

def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)

def generate_clicks(
                    p1_clicks: list, 
                    p2_clicks: list,
                    p1_releases: list,
                    p2_releases: list,
                    p1_softclicks: list,
                    p2_softclicks: list,
                    p1_softreleases: list,
                    p2_softreleases: list,
                    p1_hardclicks: list,
                    p2_hardclicks: list,
                    p1_hardreleases: list,
                    p2_hardreleases: list,

                    p1_macro: list,
                    p2_macro: list,
                    replay_fps: float,

                    enable_softclicks: bool,
                    enable_hardclicks: bool,
                    softclick_duration_option: int,
                    hardclick_duration_option: int,
                    randomize_softclicks: bool,
                    randomize_hardclicks: bool,
                    output_filename: str,
                    use_sound_pitch: bool
                ):

    output_sound = AudioSegment.empty()
    output_sound = output_sound.set_frame_rate(44100) 
    
    try:
        audio_time = (p1_macro[-1][0] / replay_fps + p1_releases[0].duration_seconds if p1_releases[0].duration_seconds != 0 else 1 + 0.2) * 1000
    except IndexError: 
        audio_time = (p2_macro[-1][0] / replay_fps + p1_releases[0].duration_seconds if p1_releases[0].duration_seconds != 0 else 1 + 0.2) * 1000
    
    output_sound += AudioSegment.silent(audio_time)
    
    last_action_time = 0

    both_players_macro = [p1_macro, p2_macro] 

    pbar = tqdm(total=len(p1_macro) + len(p2_macro), colour='green', ascii=True, desc='Progress')

    current_player = 0

    for macro in both_players_macro:
        current_player += 1 

        if current_player == 1:
            softclicks = p1_softclicks
            softreleases = p1_softreleases
            clicks = p1_clicks
            releases = p1_releases
            hardclicks = p1_hardclicks
            hardreleases = p1_hardreleases
        else:
            softclicks = p2_softclicks
            softreleases = p2_softreleases
            clicks = p2_clicks
            releases = p2_releases
            hardclicks = p2_hardclicks
            hardreleases = p2_hardreleases

        softclick_duration = softclick_duration_option
        hardclick_duration = hardclick_duration_option
        
        for action in macro:
            if randomize_softclicks:
                rs = random.randint(0, 10)
            if randomize_hardclicks:
                rh = random.randint(0, 10)
            
            if (action[0] / replay_fps * 1000 - last_action_time < softclick_duration + rs) and enable_softclicks: 
                if action[1] == 'click':
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(softclicks)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(softclicks),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                else: 

                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(softreleases)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(softreleases),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
            elif (action[0] / replay_fps * 1000 - last_action_time > hardclick_duration + rh) and enable_hardclicks:
                if action[1] == 'click':
                    if use_sound_pitch:
                        pitched_sound = random.choice(hardclicks)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)
                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        output_sound = output_sound.overlay(
                            seg=random.choice(clicks),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                else:
                    if use_sound_pitch:
                        pitched_sound = random.choice(hardreleases)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(releases),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1)
            else: 
                if action[1] == "click":
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(clicks)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(clicks),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                
                elif action[1] == "release":
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(releases)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(releases),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 

                last_action_time = action[0] / replay_fps * 1000
    
    pbar.close()

    print('\nExporting...')
    output_sound.export(output_filename, format="wav")
