import traceback
import customtkinter as ctk
from tkinter import filedialog

from utils import *
from macro_parser import parser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ZCB_GUI(ctk.CTk):
    WIDTH = 550
    HEIGHT = 250

    MACRO_PATH = None
    CLICKPACK_PATH = None
    OUTPUT_PATH = None

    P1_MACRO = None
    P2_MACRO = None
    REPLAY_FPS = None

    P1_CLICKS = None
    P1_RELEASES = None
    P1_SOFTCLICKS = None
    P1_SOFTRELEASES = None
    P2_CLICKS = None
    P2_RELEASES = None
    P2_SOFTCLICKS = None
    P2_SOFTRELEASES = None

    def __init__(self):
        super().__init__()
        
        # configure the window
        self.title("ZCB")
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # configure buttons
        self.sel_macro_btn = ctk.CTkButton(self, text="Select Macro", command=self.sel_macro)
        self.sel_macro_btn.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=(10, 0))

        self.sel_clickpack_btn = ctk.CTkButton(self, text="Select Clickpack", command=self.sel_clickpack)
        self.sel_clickpack_btn.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))

        self.sel_output_btn = ctk.CTkButton(self, text="Select Output", command=self.sel_output)
        self.sel_output_btn.grid(row=0, column=2, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure options
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 0))

        # configure options grid layout
        self.options_frame.grid_columnconfigure((0, 1), weight=1)

        # give the options frame a label
        self.options_label = ctk.CTkLabel(self.options_frame, text="Options")
        self.options_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 10))

        # pitch clicks option
        self.pitch_clicks_var = ctk.BooleanVar()
        self.pitch_clicks_cb = ctk.CTkCheckBox(self.options_frame, text="Pitch Clicks", variable=self.pitch_clicks_var)
        self.pitch_clicks_cb.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # use default softclick delay option
        self.use_default_softclick_delay_var = ctk.BooleanVar()
        self.use_default_softclick_delay_cb = ctk.CTkCheckBox(self.options_frame, text="Use Default Softclick Delay", variable=self.use_default_softclick_delay_var)
        self.use_default_softclick_delay_cb.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay option
        self.softclick_delay_var = ctk.IntVar(value=120)
        self.softclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.softclick_delay_var, placeholder_text="Softclick Delay")
        self.softclick_delay_entry.grid(row=1, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # generate button
        self.generate_btn = ctk.CTkButton(self, text="Generate", command=self.generate)
        self.generate_btn.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # disable the softclick delay entry if the use default softclick delay option is checked
        self.use_default_softclick_delay_cb.configure(command=lambda: self.softclick_delay_entry.configure(state="disabled" if self.use_default_softclick_delay_var.get() else "normal"))
    
    def sel_macro(self):
        self.MACRO_PATH = filedialog.askopenfilename(filetypes=(
            ("All files", "*.*"),
            ("MHR Json", "*.mhr.json"),
            ("TASBOT", "*.json"),
            ("Echo", "*.echo"),
            ("ZBot", "*.zbf"),
            ("ReplayBot", "*.replay"),
        ))
        log.printinfo(f"Selected macro: {self.MACRO_PATH}")
        try:
            if self.MACRO_PATH.endswith(".mhr.json"):
                f = open(self.MACRO_PATH, "r")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_mhrj(f.read())
            elif self.MACRO_PATH.endswith(".json"):
                f = open(self.MACRO_PATH, "r")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_tasbot(f.read())
            elif self.MACRO_PATH.endswith(".echo"):
                f = open(self.MACRO_PATH, "r")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_echo(f.read())
            elif self.MACRO_PATH.endswith(".zbf"):
                # since zbot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_zbot(f.read())
            elif self.MACRO_PATH.endswith(".replay"):
                # since replaybot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_rply(f.read())
            elif self.MACRO_PATH == "":
                pass
            else:
                log.printerr("Invalid macro file type! Please choose a supported macro file type.")
        except:
            log.printerr(f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
    
    def sel_clickpack(self):
        self.CLICKPACK_PATH = filedialog.askdirectory()
        log.printinfo(f"Selected clickpack: {self.CLICKPACK_PATH}")
        self.P1_CLICKS, self.P2_CLICKS, self.P1_RELEASES, self.P2_RELEASES, self.P1_SOFTCLICKS, self.P2_SOFTCLICKS, self.P1_SOFTRELEASES, self.P2_SOFTRELEASES = discover_clicks(self.CLICKPACK_PATH)
    
    def sel_output(self):
        self.OUTPUT_PATH = filedialog.asksaveasfilename(filetypes=(
            ("WAV file", "*.wav"),
            ("All files", "*.*")
        ))
        log.printinfo(f"Selected output: {self.OUTPUT_PATH}")

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

        check_softclick_delay = lambda: self.softclick_delay_var.get() if not self.use_default_softclick_delay_var.get() else "default"

        try:
            generate_clicks(
                p1_clicks=self.P1_CLICKS,
                p1_releases=self.P1_RELEASES,
                p1_softclicks=self.P1_SOFTCLICKS,
                p1_softreleases=self.P1_SOFTRELEASES,
                p2_clicks=self.P2_CLICKS,
                p2_releases=self.P2_RELEASES,
                p2_softclicks=self.P2_SOFTCLICKS,
                p2_softreleases=self.P2_SOFTRELEASES,
                p1_macro=self.P1_MACRO,
                p2_macro=self.P2_MACRO,
                replay_fps=self.REPLAY_FPS,
                softclick_duration_option=check_softclick_delay(),
                use_sound_pitch=self.pitch_clicks_var.get(),
                output_filename=self.OUTPUT_PATH
            )
            log.printsuccess("Clicks generated successfully!\nOutput: " + self.OUTPUT_PATH)
        except:
            log.printerr(f'An Error occured while generating clicks!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')

if __name__ == "__main__":
    gui = ZCB_GUI()
    gui.mainloop()