import json
import struct
from log import log

class parser:
    def parse_zbf(replay_file):
        '''
        Parses .zbf files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''

        delta = struct.unpack('f', replay_file[0:4])[0]
        speed = struct.unpack('f', replay_file[4:8])[0]
        replay_fps = 1 / delta / speed
        if replay_fps == 0:
            log.printerr("Macro corrupted.")
            input()
            exit()
        
        last_click_action = False
        last_p2_click_action = False
        p1_clicks = []
        p2_clicks = []

        i = 8
        while i < len(replay_file):
            last_frame = struct.unpack('i', replay_file[i:i+4])[0]
            last_action = replay_file[i+4] == 0x31
            is_p2 = replay_file[i+5] == 0x31
            is_action = True

            if not is_p2: # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p1_clicks.append([last_frame, 'click'])

                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    p1_clicks.append([last_frame, 'release'])
            else: # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p2_clicks.append([last_frame, 'click'])

                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    p2_clicks.append([last_frame, 'release'])
                else:
                    pass
            i += 6
        
        return p1_clicks, p2_clicks, replay_fps
    
    def parse_echo(replay_file):
        '''
        Parses .echo files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = json.loads(replay_file)
        replay_fps = replay.get('FPS')
        replay_data = replay.get('Echo Replay')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None:
            log.printerr("Macro corrupted.")
            input()
            exit()
        if replay_data is None:
            log.printerr("Empty macro.")
            input()
            exit()

        p1_clicks = []
        p2_clicks = []

        for frame in replay_data: # Iterate through every frame of the macro.
            last_frame = frame.get('Frame')
            last_action = frame.get('Hold')
            is_p2 = frame.get("Player 2")
            try:
                is_action = frame.get('Action')
            except Exception:
                is_action = True

            if not is_p2: # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p1_clicks.append([last_frame, 'click'])

                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    p1_clicks.append([last_frame, 'release'])
            else: # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p2_clicks.append([last_frame, 'click'])

                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    p2_clicks.append([last_frame, 'release'])
                else:
                    pass
        
        return p1_clicks, p2_clicks, replay_fps # Return parsed macro.

    def parse_mhrj(replay_file):
        '''
        Parses .json (mhr) files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = json.loads(replay_file)
        replay_fps = replay.get('meta').get('fps')
        replay_data = replay.get('events')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None or replay_data is None:
            log.printerr("Corrupted macro.")
            input()
            exit()

        p1_clicks = []
        p2_clicks = []

        for frame in replay_data: # Iterate through every frame of the macro.
            last_frame = frame.get('frame')
            
            is_p2 = frame.get('p2') or False
            last_action = frame.get('down')
            is_action = True

            if not is_p2: # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p1_clicks.append([last_frame, 'click'])
                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    p1_clicks.append([last_frame, 'release'])
                else:
                    pass
            else: # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p2_clicks.append([last_frame, 'click'])
                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    p2_clicks.append([last_frame, 'release'])

        return p1_clicks, p2_clicks, replay_fps

    def parse_tasbot(replay_file):
        '''
        Parses .json (tasbot) files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = json.loads(replay_file)
        replay_fps = replay.get('fps')
        replay_data = replay.get('macro')
        last_click_action = False
        last_p2_click_action = False

        if replay_fps is None or replay_data is None:
            log.printerr("Corrupted macro.")
            input()
            exit()

        p1_clicks = []
        p2_clicks = []

        for frame in replay_data: # Iterate through every frame of the macro.
            last_frame = frame.get('frame')
            
            player_1_frame = frame.get('player_1')
            player_2_frame = frame.get('player_2')

            last_p1_action = player_1_frame.get('click') == 1
            last_p2_action = player_2_frame.get('click') == 1

            if not last_click_action and last_p1_action:
                last_click_action = True
                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p1_clicks.append([last_frame, 'click'])
            elif not last_p1_action and last_click_action: # If the action is from player 1.
                last_p2_click_action = False
                p1_clicks.append([last_frame, 'release'])

            if not last_p2_click_action and last_p2_action: # If the action is from player 2.
                last_p2_click_action = True

                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p2_clicks.append([last_frame, 'click'])
            elif not last_p2_action and last_p2_click_action:
                last_click_action = False
                p2_clicks.append([last_frame, 'release'])

        return p1_clicks, p2_clicks, replay_fps