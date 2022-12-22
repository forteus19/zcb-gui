import random
from pydub import AudioSegment, effects
from tqdm import tqdm
import numpy as np

def generate_clicks(
                    p1_clicks: list, p2_clicks: list,
                    p1_releases: list, p2_releases: list,
                    p1_softclicks: list, p2_softclicks: list,
                    p1_softreleases: list, p2_softreleases: list,
                    p1_hardclicks: list, p2_hardclicks: list,
                    p1_hardreleases: list, p2_hardreleases: list,

                    actions: np.ndarray,
                    replay_fps: float,

                    enable_softclicks: bool, enable_hardclicks: bool,
                    softclick_duration_option: int, hardclick_duration_option: int,
                    randomize_softclicks: bool, randomize_hardclicks: bool,

                    output_filename: str,
                    output_format: str,
                    output_sample_rate: int,
                    output_bitrate: int,
                    use_sound_pitch: bool,
                    normalize_output: bool,
                ):
    
    millis = lambda frame, fps: frame / fps * 1000

    audio_time = millis(actions[-1, 0], replay_fps) + 1000

    output_sound = AudioSegment.silent(duration=audio_time, frame_rate=output_sample_rate)
    last_action_time = millis(actions[-1, 0], replay_fps)

    pbar = tqdm(total=len(actions), desc="Generating")

    for action in actions:
        rs = softclick_duration_option
        rs += random.randint(0, 10) if randomize_softclicks else 0
        rh = hardclick_duration_option
        rh += random.randint(0, 10) if randomize_hardclicks else 0

        for i in range(2):
            player = i + 1
            clicks = p1_clicks if player == 1 else p2_clicks
            releases = p1_releases if player == 1 else p2_releases
            softclicks = p1_softclicks if player == 1 else p2_softclicks
            softreleases = p1_softreleases if player == 1 else p2_softreleases
            hardclicks = p1_hardclicks if player == 1 else p2_hardclicks
            hardreleases = p1_hardreleases if player == 1 else p2_hardreleases
            frame = millis(action[0], replay_fps)

            if action[1]:
                if frame - last_action_time < rs and enable_softclicks:
                    output_sound = insert_click(random.choice(softclicks), millis(action[0], replay_fps), output_sound, use_sound_pitch)
                elif frame - last_action_time > rs and enable_hardclicks:
                    output_sound = insert_click(random.choice(hardclicks), millis(action[0], replay_fps), output_sound, use_sound_pitch)
                else:
                    output_sound = insert_click(random.choice(clicks), millis(action[0], replay_fps), output_sound, use_sound_pitch)
            else:
                if frame - last_action_time < rs and enable_softclicks:
                    output_sound = insert_click(random.choice(softreleases), millis(action[0], replay_fps), output_sound, use_sound_pitch)
                elif frame - last_action_time > rs and enable_hardclicks:
                    output_sound = insert_click(random.choice(hardreleases), millis(action[0], replay_fps), output_sound, use_sound_pitch)
                else:
                    output_sound = insert_click(random.choice(releases), millis(action[0], replay_fps), output_sound, use_sound_pitch)
            last_action_time = frame
            pbar.update(1)
        
        pbar.close()

        if normalize_output:
            output_sound = effects.normalize(output_sound)
        output_sound.export(out_f=output_filename, format=output_format, bitrate=output_bitrate)

def insert_click(segment, position, current, pitch_sound):
    if pitch_sound:
        pitched_sound = segment
        octaves = random.uniform(-0.1, 0.1) 
        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
        pitched_sound = pitched_sound.set_frame_rate(44100)
        
        output = current.overlay(
            seg=pitched_sound,
            position=position, 
        )
    else:
        output = current.overlay(
            seg=segment,
            position=position, 
        )
    
    return output