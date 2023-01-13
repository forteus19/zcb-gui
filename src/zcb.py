import traceback
import customtkinter as ctk
from tkinter import PhotoImage, filedialog
from os import path
from threading import Thread

from utils import *
from macro_parser import Parser
from discover_clicks import discover_clicks
from generate_clicks import generate_clicks
from log import Log


class ZCB_GUI(ctk.CTk):
    TITLE = "ZCB-GUI v1.4"
    WIDTH = 550
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
        except Exception:
            Log.printwarn("Failed to load custom theme! Falling back to default theme.")

        super().__init__()

        # configure the window
        self.title(self.TITLE)
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        # set the icon
        try:
            self.iconphoto(False, PhotoImage(file=resource_path(path.join("assets", "icon.png"))))
        except Exception:
            Log.printwarn("Failed to load custom icon! Falling back to default icon.")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)

        # configure the header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure header grid layout
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

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
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(2, weight=1)

        # give the options frame a label
        self.options_label = ctk.CTkLabel(self.options_frame, text="Options", font=("Segoe UI", 14, "bold"))
        self.options_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 10))

        # enable softclicks option
        self.enable_softclicks_var = ctk.BooleanVar()
        self.enable_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Softclicks",
                                                    variable=self.enable_softclicks_var)
        self.enable_softclicks_cb.grid(row=2, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # enable hardclicks option
        self.enable_hardclicks_var = ctk.BooleanVar()
        self.enable_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Hardclicks",
                                                    variable=self.enable_hardclicks_var)
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
        self.randomize_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Softclicks",
                                                       variable=self.randomize_softclicks_var)
        self.randomize_softclicks_cb.grid(row=3, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay option
        self.softclick_delay_var = ctk.IntVar(value=120)
        self.softclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.softclick_delay_var,
                                                  placeholder_text="Softclick Delay")
        self.softclick_delay_entry.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay label
        self.hardclick_delay_label = ctk.CTkLabel(self.options_frame, text="Hardclick Delay")
        self.hardclick_delay_label.grid(row=2, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # randomize hardclicks option
        self.randomize_hardclicks_var = ctk.BooleanVar()
        self.randomize_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Hardclicks",
                                                       variable=self.randomize_hardclicks_var)
        self.randomize_hardclicks_cb.grid(row=5, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay option
        self.hardclick_delay_var = ctk.IntVar(value=360)
        self.hardclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.hardclick_delay_var,
                                                  placeholder_text="Hardclick Delay")
        self.hardclick_delay_entry.grid(row=2, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output sample rate label
        self.output_sample_rate_label = ctk.CTkLabel(self.options_frame, text="Sample Rate")
        self.output_sample_rate_label.grid(row=3, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output sample rate option
        self.output_sample_rate_var = ctk.IntVar(value=44100)
        self.output_sample_rate_entry = ctk.CTkEntry(self.options_frame, textvariable=self.output_sample_rate_var,
                                                     placeholder_text="Sample Rate")
        self.output_sample_rate_entry.grid(row=3, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output bitrate label
        self.output_bitrate_label = ctk.CTkLabel(self.options_frame, text="Bitrate")
        self.output_bitrate_label.grid(row=4, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output bitrate option
        self.output_bitrate_var = ctk.IntVar(value=256)
        self.output_bitrate_entry = ctk.CTkEntry(self.options_frame, textvariable=self.output_bitrate_var,
                                                 placeholder_text="Bitrate")
        self.output_bitrate_entry.grid(row=4, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output format label
        self.output_format_label = ctk.CTkLabel(self.options_frame, text="Format")
        self.output_format_label.grid(row=5, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # output format option
        self.output_format_var = ctk.StringVar(value="WAV")
        self.output_format_entry = ctk.CTkComboBox(self.options_frame, variable=self.output_format_var,
                                                   values=["WAV", "MP3"])
        self.output_format_entry.grid(row=5, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # normalize output option
        self.normalize_output_var = ctk.BooleanVar()
        self.normalize_output_cb = ctk.CTkCheckBox(self.options_frame, text="Normalize Output",
                                                   variable=self.normalize_output_var)
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
        self.macro_frame.grid_columnconfigure(0, weight=1)
        self.macro_frame.grid_columnconfigure(1, weight=1)
        self.macro_frame.grid_columnconfigure(2, weight=1)

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
        if self.MACRO_PATH in ("", ()):
            self.MACRO_PATH = None
            return
        Log.printinfo(f"Selected macro: {self.MACRO_PATH}")
        try:
            if self.MACRO_PATH.endswith(".mhr.json"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_mhrj(f.read())
                self.macro_format_label.configure(text=f"Format: MHR Json")
            elif self.MACRO_PATH.endswith(".mhr"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_mhr_bin(f.read())
                self.macro_format_label.configure(text=f"Format: MHR")
            elif self.MACRO_PATH.endswith(".json"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_tasbot(f.read())
                self.macro_format_label.configure(text=f"Format: TASBOT")
            elif self.MACRO_PATH.endswith(".echo"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_echo(f.read())
                self.macro_format_label.configure(text=f"Format: Echo")
            elif self.MACRO_PATH.endswith(".zbf"):
                # since zbot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_zbf(f.read())
                self.macro_format_label.configure(text=f"Format: ZBot")
            elif self.MACRO_PATH.endswith(".replay"):
                # since replaybot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_rply(f.read())
                self.macro_format_label.configure(text=f"Format: ReplayBot")
            elif self.MACRO_PATH.endswith(".txt"):
                f = open(self.MACRO_PATH, "r")
                self.ACTIONS, self.REPLAY_FPS = Parser.parse_txt(f.read())
                self.macro_format_label.configure(text=f"Format: Plain Text")
            else:
                Log.printerr("Invalid macro file type! Please choose a supported macro file type.")
                return
        except Exception:
            Log.printerr(
                f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
            return

        f.close()

        self.macro_actions_label.configure(text=f"Actions: {len(self.ACTIONS)}")
        self.replay_fps_label.configure(text=f"FPS: {round(self.REPLAY_FPS)}")

    def sel_clickpack(self):
        self.CLICKPACK_PATH = filedialog.askdirectory()
        if self.CLICKPACK_PATH in ("", ()):
            self.CLICKPACK_PATH = None
            return
        self.P1_CLICKS, self.P2_CLICKS, self.P1_RELEASES, self.P2_RELEASES, self.P1_SOFTCLICKS, self.P2_SOFTCLICKS, self.P1_SOFTRELEASES, self.P2_SOFTRELEASES, self.P1_HARDCLICKS, self.P2_HARDCLICKS, self.P1_HARDRELEASES, self.P2_HARDRELEASES = discover_clicks(
            self.CLICKPACK_PATH)

    def sel_output(self):
        self.OUTPUT_PATH = filedialog.asksaveasfilename(filetypes=(
            ("WAV file", "*.wav"),
            ("MP3 file", "*.mp3"),
            ("All files", "*.*")
        ))
        if self.OUTPUT_PATH in ("", ()):
            self.OUTPUT_PATH = None
            return
        extension = f".{self.output_format_var.get().lower()}"
        if not self.OUTPUT_PATH.endswith(extension):
            self.OUTPUT_PATH += extension
        Log.printinfo(f"Selected output path: {self.OUTPUT_PATH}")

    def generate(self):
        if self.MACRO_PATH is None:
            Log.printerr("Please select a macro!")
            return
        if self.CLICKPACK_PATH is None:
            Log.printerr("Please select a clickpack!")
            return
        if self.OUTPUT_PATH is None:
            Log.printerr("Please select an output path!")
            return

        try:
            t = Thread(target=generate_clicks, args=(
                self.P1_CLICKS,
                self.P2_CLICKS,
                self.P1_RELEASES,
                self.P2_RELEASES,
                self.P1_SOFTCLICKS,
                self.P2_SOFTCLICKS,
                self.P1_SOFTRELEASES,
                self.P2_SOFTRELEASES,
                self.P1_HARDCLICKS,
                self.P2_HARDCLICKS,
                self.P1_HARDRELEASES,
                self.P2_HARDRELEASES,
                self.ACTIONS,
                self.REPLAY_FPS,
                self.enable_softclicks_var.get(),
                self.enable_hardclicks_var.get(),
                self.softclick_delay_var.get(),
                self.hardclick_delay_var.get(),
                self.randomize_softclicks_var.get(),
                self.randomize_hardclicks_var.get(),
                self.OUTPUT_PATH,
                self.output_format_var.get().lower(),
                self.output_sample_rate_var.get(),
                self.output_bitrate_var.get(),
                self.pitch_clicks_var.get(),
                self.normalize_output_var.get(),
            ))
            t.start()
        except KeyboardInterrupt:
            Log.printinfo("Click generation cancelled!")
        except Exception:
            Log.printerr(
                f'An Error occured while generating clicks!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')


if __name__ == "__main__":
    check_for_updates()

    gui = ZCB_GUI()
    gui.mainloop()
