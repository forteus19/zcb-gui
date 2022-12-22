import traceback
import customtkinter as ctk
from tkinter import PhotoImage, filedialog
from os import path

from utils import *
from macro_parser import parser
from discover_clicks import discover_clicks
from generate_clicks import generate_clicks
from log import log

class ZCB_GUI(ctk.CTk):
    WIDTH = 600
    HEIGHT = 582

    MACRO_PATH = None
    CLICKPACK_PATH = None
    OUTPUT_PATH = None

    ACTIONS = None
    REPLAY_FPS = None

    P1_CLICKS = None
    P1_RELEASES = None
    P1_SOFTCLICKS = None
    P1_SOFTRELEASES = None
    P1_HARDCLICKS = None
    P1_HARDRELEASES = None

    P2_CLICKS = None
    P2_RELEASES = None
    P2_SOFTCLICKS = None
    P2_SOFTRELEASES = None
    P2_HARDCLICKS = None
    P2_HARDRELEASES = None

    log_textbox = None

    def __init__(self):
        ctk.set_appearance_mode("dark")
        try:
            ctk.set_default_color_theme(resource_path(path.join("assets", "theme.json")))
        except:
            log.printwarn("Failed to load custom theme! Falling back to default theme.")

        super().__init__()

        # configure the window
        self.title("ZCB-GUI v1.4-alpha")
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        # set the icon
        try:
            self.iconphoto(False, PhotoImage(file=resource_path(path.join("assets", "icon.png"))))
        except:
            log.printwarn("Failed to load custom icon! Falling back to default icon.")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)

        # configure the header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure header grid layout
        self.header_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # give the header frame a label
        self.header_label = ctk.CTkLabel(self.header_frame, text="Load Files", font=("Segoe UI", 14, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        # configure buttons
        self.sel_macro_btn = ctk.CTkButton(self.header_frame, text="Select Macro", command=self.sel_macro)
        self.sel_macro_btn.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(10, 10))

        self.sel_clickpack_btn = ctk.CTkButton(self.header_frame, text="Select Clickpack", command=self.sel_clickpack)
        self.sel_clickpack_btn.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 10))

        self.sel_output_btn = ctk.CTkButton(self.header_frame, text="Select Output", command=self.sel_output)
        self.sel_output_btn.grid(row=1, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # configure generation options frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure options grid layout
        self.options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # give the options frame a label
        self.options_label = ctk.CTkLabel(self.options_frame, text="Options", font=("Segoe UI", 14, "bold"))
        self.options_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 10))

        # enable softclicks option
        self.enable_softclicks_var = ctk.BooleanVar()
        self.enable_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Softclicks", variable=self.enable_softclicks_var)
        self.enable_softclicks_cb.grid(row=2, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # enable hardclicks option
        self.enable_hardclicks_var = ctk.BooleanVar()
        self.enable_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Hardclicks", variable=self.enable_hardclicks_var)
        self.enable_hardclicks_cb.grid(row=4, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # pitch clicks option
        self.pitch_clicks_var = ctk.BooleanVar()
        self.pitch_clicks_cb = ctk.CTkCheckBox(self.options_frame, text="Pitch Clicks", variable=self.pitch_clicks_var)
        self.pitch_clicks_cb.grid(row=1, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay label
        self.softclick_delay_label = ctk.CTkLabel(self.options_frame, text="Softclick Delay")
        self.softclick_delay_label.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # randomize softclicks option
        self.randomize_softclicks_var = ctk.BooleanVar()
        self.randomize_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Softclicks", variable=self.randomize_softclicks_var)
        self.randomize_softclicks_cb.grid(row=3, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay option
        self.softclick_delay_var = ctk.IntVar(value=120)
        self.softclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.softclick_delay_var, placeholder_text="Softclick Delay")
        self.softclick_delay_entry.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay label
        self.hardclick_delay_label = ctk.CTkLabel(self.options_frame, text="Hardclick Delay")
        self.hardclick_delay_label.grid(row=2, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # randomize hardclicks option
        self.randomize_hardclicks_var = ctk.BooleanVar()
        self.randomize_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Hardclicks", variable=self.randomize_hardclicks_var)
        self.randomize_hardclicks_cb.grid(row=5, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay option
        self.hardclick_delay_var = ctk.IntVar(value=360)
        self.hardclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.hardclick_delay_var, placeholder_text="Hardclick Delay")
        self.hardclick_delay_entry.grid(row=2, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output sample rate label
        self.output_sample_rate_label = ctk.CTkLabel(self.options_frame, text="Sample Rate")
        self.output_sample_rate_label.grid(row=3, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output sample rate option
        self.output_sample_rate_var = ctk.IntVar(value=44100)
        self.output_sample_rate_entry = ctk.CTkEntry(self.options_frame, textvariable=self.output_sample_rate_var, placeholder_text="Sample Rate")
        self.output_sample_rate_entry.grid(row=3, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output bitrate label
        self.output_bitrate_label = ctk.CTkLabel(self.options_frame, text="Bitrate")
        self.output_bitrate_label.grid(row=4, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output bitrate option
        self.output_bitrate_var = ctk.IntVar(value=256)
        self.output_bitrate_entry = ctk.CTkEntry(self.options_frame, textvariable=self.output_bitrate_var, placeholder_text="Bitrate")
        self.output_bitrate_entry.grid(row=4, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output format label
        self.output_format_label = ctk.CTkLabel(self.options_frame, text="Format")
        self.output_format_label.grid(row=5, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output format option
        self.output_format_var = ctk.StringVar(value="WAV")
        self.output_format_entry = ctk.CTkComboBox(self.options_frame, variable=self.output_format_var, values=["WAV", "MP3"])
        self.output_format_entry.grid(row=5, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # normalize output option
        self.normalize_output_var = ctk.BooleanVar()
        self.normalize_output_cb = ctk.CTkCheckBox(self.options_frame, text="Normalize Output (recommended)", variable=self.normalize_output_var)
        self.normalize_output_cb.grid(row=6, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # defaults
        self.enable_softclicks_cb.select()
        self.enable_hardclicks_cb.select()
        self.pitch_clicks_cb.select()
        self.randomize_softclicks_cb.select()
        self.randomize_hardclicks_cb.select()

        # loaded macro information frame
        self.macro_frame = ctk.CTkFrame(self)
        self.macro_frame.grid(row=3, column=0, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure macro grid layout
        self.macro_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # give the macro frame a label
        self.macro_label = ctk.CTkLabel(self.macro_frame, text="Macro Info", font=("Segoe UI", 14, "bold"))
        self.macro_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 10))

        # macro format label
        self.macro_format_label = ctk.CTkLabel(self.macro_frame, text="Format:")
        self.macro_format_label.grid(row=1, column=0, sticky="nsw", padx=(10, 10), pady=(0, 10))

        # replay fps label
        self.replay_fps_label = ctk.CTkLabel(self.macro_frame, text="FPS:")
        self.replay_fps_label.grid(row=1, column=1, sticky="nsw", padx=(10, 10), pady=(0, 10))

        # macro actions label
        self.macro_actions_label = ctk.CTkLabel(self.macro_frame, text="Actions:")
        self.macro_actions_label.grid(row=1, column=2, sticky="nsw", padx=(10, 10), pady=(0, 10))

        # generate button
        self.generate_btn = ctk.CTkButton(self, text="Generate", command=self.generate)
        self.generate_btn.grid(row=4, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
    
    def sel_macro(self):
        self.MACRO_PATH = filedialog.askopenfilename(filetypes=(
            ("All files", "*.*"),
            ("MHR Json", "*.mhr.json"),
            ("TASBOT", "*.json"),
            ("Echo", "*.echo"),
            ("ZBot", "*.zbf"),
            ("ReplayBot", "*.replay"),
            ("Plain Text", "*.txt")
        ))
        if self.MACRO_PATH in ("", ()): return
        log.printinfo(f"Selected macro: {self.MACRO_PATH}")
        try:
            if self.MACRO_PATH.endswith(".mhr.json"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_mhrj(f.read())
                self.macro_format_label.configure(text=f"Format: MHR Json")
            elif self.MACRO_PATH.endswith(".json"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_tasbot(f.read())
                self.macro_format_label.configure(text=f"Format: TASBOT")
            elif self.MACRO_PATH.endswith(".echo"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_echo(f.read())
                self.macro_format_label.configure(text=f"Format: Echo")
            elif self.MACRO_PATH.endswith(".zbf"):
                # since zbot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_zbf(f.read())
                self.macro_format_label.configure(text=f"Format: ZBot")
            elif self.MACRO_PATH.endswith(".replay"):
                # since replaybot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_rply(f.read())
                self.macro_format_label.configure(text=f"Format: ReplayBot")
            elif self.MACRO_PATH.endswith(".txt"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = parser.parse_txt(f.read())
                self.macro_format_label.configure(text=f"Format: Plain Text")
            else:
                log.printerr("Invalid macro file type! Please choose a supported macro file type.")
                return
        except:
            log.printerr(f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
            return
        
        self.macro_actions_label.configure(text=f"Actions: {len(self.ACTIONS)}")
        self.replay_fps_label.configure(text=f"FPS: {round(self.REPLAY_FPS)}")
    
    def sel_clickpack(self):
        self.CLICKPACK_PATH = filedialog.askdirectory()
        if self.CLICKPACK_PATH in ("", ()): return
        self.P1_CLICKS, self.P2_CLICKS, self.P1_RELEASES, self.P2_RELEASES, self.P1_SOFTCLICKS, self.P2_SOFTCLICKS, self.P1_SOFTRELEASES, self.P2_SOFTRELEASES, self.P1_HARDCLICKS, self.P2_HARDCLICKS, self.P1_HARDRELEASES, self.P2_HARDRELEASES = discover_clicks(self.CLICKPACK_PATH)
    
    def sel_output(self):
        self.OUTPUT_PATH = filedialog.asksaveasfilename(filetypes=(
            ("WAV file", "*.wav"),
            ("MP3 file", "*.mp3"),
            ("All files", "*.*")
        ))
        if self.OUTPUT_PATH in ("", ()): return
        extension = f".{self.output_format_var.get().lower()}"
        if not self.OUTPUT_PATH.endswith(extension):
            self.OUTPUT_PATH += extension
        log.printinfo(f"Selected output path: {self.OUTPUT_PATH}")

    def generate(self):
        if self.MACRO_PATH in ("", None):
            log.printerr("Please select a macro!")
            return
        if self.CLICKPACK_PATH in ("", None):
            log.printerr("Please select a clickpack!")
            return
        if self.OUTPUT_PATH in ("", None):
            log.printerr("Please select an output path!")
            return

        try:
            generate_clicks(
                p1_clicks=self.P1_CLICKS,
                p1_releases=self.P1_RELEASES,
                p1_softclicks=self.P1_SOFTCLICKS,
                p1_softreleases=self.P1_SOFTRELEASES,
                p1_hardclicks=self.P1_HARDCLICKS,
                p1_hardreleases=self.P1_HARDRELEASES,
                p2_clicks=self.P2_CLICKS,
                p2_releases=self.P2_RELEASES,
                p2_softclicks=self.P2_SOFTCLICKS,
                p2_softreleases=self.P2_SOFTRELEASES,
                p2_hardclicks=self.P2_HARDCLICKS,
                p2_hardreleases=self.P2_HARDRELEASES,
                actions=self.ACTIONS,
                replay_fps=self.REPLAY_FPS,
                enable_softclicks=self.enable_softclicks_var.get(),
                enable_hardclicks=self.enable_hardclicks_var.get(),
                softclick_duration_option=self.softclick_delay_var.get(),
                hardclick_duration_option=self.hardclick_delay_var.get(),
                randomize_softclicks=self.randomize_softclicks_var.get(),
                randomize_hardclicks=self.randomize_hardclicks_var.get(),
                use_sound_pitch=self.pitch_clicks_var.get(),
                output_filename=self.OUTPUT_PATH,
                output_format=self.output_format_var.get().lower(),
                output_sample_rate=self.output_sample_rate_var.get(),
                output_bitrate=self.output_bitrate_var.get(),
                normalize_output=self.normalize_output_var.get(),
            )
            log.printsuccess("Clicks generated successfully!\nOutput: " + self.OUTPUT_PATH)
        except:
            log.printerr(f'An Error occured while generating clicks!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')

if __name__ == "__main__":
    check_for_updates()
    
    gui = ZCB_GUI()
    gui.mainloop()