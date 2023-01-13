from json import loads
from struct import unpack
from log import Log
import numpy as np


class Parser:
    @staticmethod
    def parse_zbf(replay_file):
        Log.printinfo("Parsing ZBot file...")
        delta = unpack('f', replay_file[0:4])[0]
        speed = unpack('f', replay_file[4:8])[0]
        replay_fps = 1 / delta / speed
        if replay_fps == 0:
            Log.printerr("Macro corrupted.")

        last_click_action = False
        last_p2_click_action = False
        actions = np.array([], dtype=np.int32).reshape(0, 3)

        i = 8
        while i < len(replay_file):
            last_frame = unpack('i', replay_file[i:i + 4])[0]
            last_action = replay_file[i + 4] == 0x31
            is_p2 = replay_file[i + 5] == 0x31

            if not is_p2:  # If the action is from player 1.
                if last_action and not last_click_action:
                    last_click_action = True
                    '''
                    Xd array:
                    [[frame, True or False], ...]
                    '''
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)

                elif not last_action and last_click_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
            else:  # If the action is from player 2.
                if last_action and not last_p2_click_action:
                    last_p2_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)

                elif not last_action and last_p2_click_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)
                else:
                    pass
            i += 6

        Log.printsuccess("Parsed ZBot file.")
        return actions, replay_fps

    @staticmethod
    def parse_echo(replay_file):
        Log.printinfo("Parsing Echo file...")
        # Define basic info.
        replay = loads(replay_file)
        replay_fps = replay.get('FPS')
        replay_data = replay.get('Echo Replay')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None:
            Log.printerr("Macro corrupted.")
        if replay_data is None:
            Log.printerr("Empty macro.")

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        for frame in replay_data:  # Iterate through every frame of the macro.
            last_frame = frame.get('Frame')
            last_action = frame.get('Hold')
            is_p2 = frame.get("Player 2")
            try:
                is_action = frame.get('Action')
            except KeyError:
                is_action = True

            if not is_p2:  # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)

                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
            else:  # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)

                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)
                else:
                    pass

        Log.printsuccess("Parsed Echo file.")
        return actions, replay_fps  # Return parsed macro.

    @staticmethod
    def parse_mhrj(replay_file):
        Log.printinfo("Parsing MHR Json file...")
        '''
        Parses .json (mhr) files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = loads(replay_file)
        replay_fps = replay.get('meta').get('fps')
        replay_data = replay.get('events')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None or replay_data is None:
            Log.printerr("Corrupted macro.")

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        for frame in replay_data:  # Iterate through every frame of the macro.
            last_frame = frame.get('frame')

            is_p2 = frame.get('p2') or False
            last_action = frame.get('down')
            is_action = True

            if not is_p2:  # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)
                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
                else:
                    pass
            else:  # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)
                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)

        Log.printsuccess("Parsed MHR Json file.")
        return actions, replay_fps  # Return parsed macro.

    @staticmethod
    def parse_tasbot(replay_file):
        Log.printinfo("Parsing TASBOT file...")
        # Define basic info.
        replay = loads(replay_file)
        replay_fps = replay.get('fps')
        replay_data = replay.get('macro')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None or replay_data is None:
            Log.printerr("Corrupted macro.")

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        for frame in replay_data:  # Iterate through every frame of the macro.
            last_frame = frame.get('frame')

            player_1_frame = frame.get('player_1')
            player_2_frame = frame.get('player_2')

            last_p1_action = player_1_frame.get('click') == 1
            last_p2_action = player_2_frame.get('click') == 1

            if not last_click_action and last_p1_action:
                last_click_action = True
                actions = np.append(actions, [[last_frame, True, 1]], axis=0)
            elif not last_p1_action and last_click_action:  # If the action is from player 1.
                last_p2_click_action = False
                actions = np.append(actions, [[last_frame, False, 1]], axis=0)

            if not last_p2_click_action and last_p2_action:  # If the action is from player 2.
                last_p2_click_action = True
                actions = np.append(actions, [[last_frame, True, 2]], axis=0)
            elif not last_p2_action and last_p2_click_action:
                last_click_action = False
                actions = np.append(actions, [[last_frame, False, 2]], axis=0)

        Log.printsuccess("Parsed TASBOT file.")
        return actions, replay_fps

    @staticmethod
    def parse_rply(replay_file):
        Log.printinfo("Parsing ReplayBot file...")
        if unpack('4s', replay_file[0:4])[0] != b'RPLY':
            Log.printerr("Macro is not a ReplayBot macro.")
            return None, None, None
        if replay_file[5] != 0x01:
            Log.printerr("ZCB cannot process Xpos macros.")
            return None, None, None

        replay_fps = unpack('f', replay_file[6:10])[0]
        replay_data = replay_file[10:]

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        last_click_action = False
        last_p2_click_action = False

        # each frame is 5 bytes
        '''
        Frame format:
        Frame: int (4 bytes)
        Player/down: bitwise combination (0bXY)
        X: 0: player1, 1: player2
        Y: 0: release, 1: click
        '''
        for frame in range(0, len(replay_data), 5):  # Iterate through every frame of the macro.
            last_frame: int = unpack('i', replay_data[frame:frame + 4])[0]

            # true if the byte is 0x02 or 0x03
            is_p2: bool = unpack('b', replay_data[frame + 4:frame + 5])[0] & 0b10
            # true if the byte is 0x01 or 0x03
            last_action: bool = unpack('b', replay_data[frame + 4:frame + 5])[0] & 0b01

            if not is_p2:
                if last_action and not last_click_action:
                    last_click_action = True
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)
                elif not last_action and last_click_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
                else:
                    pass
            else:
                if last_action and not last_p2_click_action:
                    last_p2_click_action = True
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)
                elif not last_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)
                else:
                    pass

        Log.printsuccess("Parsed ReplayBot file.")
        return actions, replay_fps

    @staticmethod
    def parse_txt(replay_file: str):
        Log.printinfo("Parsing plain text file...")
        lines = replay_file.splitlines()
        replay_fps = int(lines[0])
        replay_data = lines[1:]
        last_click_action = False
        last_p2_click_action = False

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        for frame in replay_data:  # Iterate through every frame of the macro.
            parts = frame.split(' ')
            last_frame = int(parts[0])
            is_p2 = parts[2] == '1'
            last_action = parts[1] == '1'

            if not is_p2:
                if last_action and not last_click_action:
                    last_click_action = True
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)
                elif not last_action and last_click_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
                else:
                    pass
            else:
                if last_action and not last_p2_click_action:
                    last_p2_click_action = True
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)
                elif not last_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)
                else:
                    pass

        Log.printsuccess("Parsed plain text file.")
        return actions, replay_fps

    @staticmethod
    def parse_mhr_bin(replay_file: str):
        Log.printinfo("Parsing MHR binary file...")
        if unpack('7s', replay_file[0:7])[0] != b'HACKPRO':
            Log.printerr("Macro is not a MHR binary macro.")
            return None, None, None

        replay_fps = unpack('i', replay_file[12:16])[0]
        replay_data = replay_file[32:]

        actions = np.array([], dtype=np.int32).reshape(0, 3)

        last_click_action = False
        last_p2_click_action = False

        for frame in range(0, len(replay_data), 32):  # each frame is 32 bytes
            last_frame = unpack('i', replay_data[frame + 4:frame + 8])[0]
            is_p2 = unpack('b', replay_data[frame + 2:frame + 3])[0] == 1
            last_action = unpack('b', replay_data[frame + 3:frame + 4])[0] == 1

            if not is_p2:
                if last_action and not last_click_action:
                    last_click_action = True
                    actions = np.append(actions, [[last_frame, True, 1]], axis=0)
                elif not last_action and last_click_action:
                    last_click_action = False
                    actions = np.append(actions, [[last_frame, False, 1]], axis=0)
                else:
                    pass
            else:
                if last_action and not last_p2_click_action:
                    last_p2_click_action = True
                    actions = np.append(actions, [[last_frame, True, 2]], axis=0)
                elif not last_action:
                    last_p2_click_action = False
                    actions = np.append(actions, [[last_frame, False, 2]], axis=0)
                else:
                    pass

        Log.printsuccess("Parsed MHR binary file.")
        return actions, replay_fps
