import random
from pydub import AudioSegment, effects
from tqdm import tqdm
from log import Log
from concurrent import futures


def generate_clicks(
        p1_clicks: list, p2_clicks: list,
        p1_releases: list, p2_releases: list,
        p1_softclicks: list, p2_softclicks: list,
        p1_softreleases: list, p2_softreleases: list,
        p1_hardclicks: list, p2_hardclicks: list,
        p1_hardreleases: list, p2_hardreleases: list,

        actions,
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

    try:
        for action in actions:
            rs = softclick_duration_option
            rs += random.randint(0, 10) if randomize_softclicks else 0
            rh = hardclick_duration_option
            rh += random.randint(0, 10) if randomize_hardclicks else 0

            clicks = p2_clicks if action[2] else p1_clicks
            releases = p2_releases if action[2] else p1_releases
            softclicks = p2_softclicks if action[2] else p1_softclicks
            softreleases = p2_softreleases if action[2] else p1_softreleases
            hardclicks = p2_hardclicks if action[2] else p1_hardclicks
            hardreleases = p2_hardreleases if action[2] else p1_hardreleases

            frame = millis(action[0], replay_fps)

            is_softclick = frame - last_action_time < rs and enable_softclicks
            is_hardclick = frame - last_action_time > rh and enable_hardclicks

            executer = futures.ThreadPoolExecutor()

            if action[1]:
                if is_softclick:
                    future = executer.submit(insert_click, random.choice(softclicks), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
                elif is_hardclick:
                    future = executer.submit(insert_click, random.choice(hardclicks), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
                else:
                    future = executer.submit(insert_click, random.choice(clicks), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
            else:
                if is_softclick:
                    future = executer.submit(insert_click, random.choice(softreleases), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
                elif is_hardclick:
                    future = executer.submit(insert_click, random.choice(hardreleases), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
                else:
                    future = executer.submit(insert_click, random.choice(releases), millis(action[0], replay_fps),
                                             output_sound, use_sound_pitch)
                    output_sound = future.result()
            last_action_time = frame
            pbar.update(1)
    except KeyboardInterrupt:
        Log.printinfo("Click generation cancelled!")
        return
    except RuntimeError:
        Log.printwarn(
            "Click generation ran into a runtime error!\nThis was likely caused by an interupt, and since this is non-fatal, the program will exit normally.")
        return

    pbar.close()
    if normalize_output:
        output_sound = effects.normalize(output_sound)
    output_sound.export(out_f=output_filename, format=output_format, bitrate=output_bitrate)
    Log.printsuccess(f"Generated clicks successfully! ({output_filename})")


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
