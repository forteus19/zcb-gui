import traceback
import customtkinter as ctk
from tkinter import PhotoImage, filedialog

from utils import *
from macro_parser import parser
from discover_clicks import discover_clicks
from log import log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(path.join(get_script_path(), "assets", "theme.json"))

class ZCB_GUI(ctk.CTk):
    WIDTH = 550
    HEIGHT = 380

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
    P1_HARDCLICKS = None
    P1_HARDRELEASES = None

    P2_CLICKS = None
    P2_RELEASES = None
    P2_SOFTCLICKS = None
    P2_SOFTRELEASES = None
    P2_HARDCLICKS = None
    P2_HARDRELEASES = None

    def __init__(self):
        super().__init__()
        
        # configure the window
        self.title("ZCB")
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        # set the icon
        self.iconphoto(False, PhotoImage(file=path.join(get_script_path(), "assets", "icon.png")))

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
        self.options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # give the options frame a label
        self.options_label = ctk.CTkLabel(self.options_frame, text="Options", font=("Segoe UI", 14, "bold"))
        self.options_label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(10, 10))

        # enable softclicks option
        self.enable_softclicks_var = ctk.BooleanVar()
        self.enable_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Softclicks", variable=self.enable_softclicks_var)
        self.enable_softclicks_cb.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # enable hardclicks option
        self.enable_hardclicks_var = ctk.BooleanVar()
        self.enable_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Enable Hardclicks", variable=self.enable_hardclicks_var)
        self.enable_hardclicks_cb.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # pitch clicks option
        self.pitch_clicks_var = ctk.BooleanVar()
        self.pitch_clicks_cb = ctk.CTkCheckBox(self.options_frame, text="Pitch Clicks", variable=self.pitch_clicks_var)
        self.pitch_clicks_cb.grid(row=1, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay label
        self.softclick_delay_label = ctk.CTkLabel(self.options_frame, text="Softclick Delay")
        self.softclick_delay_label.grid(row=2, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # randomize softclicks option
        self.randomize_softclicks_var = ctk.BooleanVar()
        self.randomize_softclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Softclicks", variable=self.randomize_softclicks_var)
        self.randomize_softclicks_cb.grid(row=2, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # softclick delay option
        self.softclick_delay_var = ctk.IntVar(value=120)
        self.softclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.softclick_delay_var, placeholder_text="Softclick Delay")
        self.softclick_delay_entry.grid(row=2, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay label
        self.hardclick_delay_label = ctk.CTkLabel(self.options_frame, text="Hardclick Delay")
        self.hardclick_delay_label.grid(row=3, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # randomize hardclicks option
        self.randomize_hardclicks_var = ctk.BooleanVar()
        self.randomize_hardclicks_cb = ctk.CTkCheckBox(self.options_frame, text="Randomize Hardclicks", variable=self.randomize_hardclicks_var)
        self.randomize_hardclicks_cb.grid(row=3, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # hardclick delay option
        self.hardclick_delay_var = ctk.IntVar(value=360)
        self.hardclick_delay_entry = ctk.CTkEntry(self.options_frame, textvariable=self.hardclick_delay_var, placeholder_text="Hardclick Delay")
        self.hardclick_delay_entry.grid(row=3, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # defaults
        self.enable_softclicks_cb.select()
        self.enable_hardclicks_cb.select()
        self.pitch_clicks_cb.select()
        self.randomize_softclicks_cb.select()
        self.randomize_hardclicks_cb.select()

        # loaded macro information frame
        self.macro_frame = ctk.CTkFrame(self)
        self.macro_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 0))

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
        self.generate_btn.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))
    
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
                self.macro_format_label.configure(text=f"Format: MHR Json")
            elif self.MACRO_PATH.endswith(".json"):
                f = open(self.MACRO_PATH, "r")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_tasbot(f.read())
                self.macro_format_label.configure(text=f"Format: TASBOT")
            elif self.MACRO_PATH.endswith(".echo"):
                f = open(self.MACRO_PATH, "r")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_echo(f.read())
                self.macro_format_label.configure(text=f"Format: Echo")
            elif self.MACRO_PATH.endswith(".zbf"):
                # since zbot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_zbot(f.read())
                self.macro_format_label.configure(text=f"Format: ZBot")
            elif self.MACRO_PATH.endswith(".replay"):
                # since replaybot files are binary, we need to open them in binary mode
                f = open(self.MACRO_PATH, "rb")
                self.P1_MACRO, self.P2_MACRO, self.REPLAY_FPS = parser.parse_rply(f.read())
                self.macro_format_label.configure(text=f"Format: ReplayBot")
            elif self.MACRO_PATH == "":
                pass
            else:
                log.printerr("Invalid macro file type! Please choose a supported macro file type.")
            
            self.replay_fps_label.configure(text=f"FPS: {self.REPLAY_FPS}")
            self.macro_actions_label.configure(text=f"Actions: {len(self.P1_MACRO) + len(self.P2_MACRO)}")
        except:
            log.printerr(f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
    
    def sel_clickpack(self):
        self.CLICKPACK_PATH = filedialog.askdirectory()
        if self.CLICKPACK_PATH == "": return
        log.printinfo(f"Selected clickpack: {self.CLICKPACK_PATH}")
        self.P1_CLICKS, self.P2_CLICKS, self.P1_RELEASES, self.P2_RELEASES, self.P1_SOFTCLICKS, self.P2_SOFTCLICKS, self.P1_SOFTRELEASES, self.P2_SOFTRELEASES, self.P1_HARDCLICKS, self.P2_HARDCLICKS, self.P1_HARDRELEASES, self.P2_HARDRELEASES = discover_clicks(self.CLICKPACK_PATH)
    
    def sel_output(self):
        self.OUTPUT_PATH = filedialog.asksaveasfilename(filetypes=(
            ("WAV file", "*.wav"),
            ("All files", "*.*")
        ))
        if not self.OUTPUT_PATH.endswith(".wav"):
            self.OUTPUT_PATH += ".wav"
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
                p1_macro=self.P1_MACRO,
                p2_macro=self.P2_MACRO,
                replay_fps=self.REPLAY_FPS,
                enable_softclicks=self.enable_softclicks_var.get(),
                enable_hardclicks=self.enable_hardclicks_var.get(),
                softclick_duration_option=self.softclick_delay_var.get(),
                hardclick_duration_option=self.hardclick_delay_var.get(),
                randomize_softclicks=self.randomize_softclicks_var.get(),
                randomize_hardclicks=self.randomize_hardclicks_var.get(),
                use_sound_pitch=self.pitch_clicks_var.get(),
                output_filename=self.OUTPUT_PATH
            )
            log.printsuccess("Clicks generated successfully!\nOutput: " + self.OUTPUT_PATH)
        except:
            log.printerr(f'An Error occured while generating clicks!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')

if __name__ == "__main__":
    gui = ZCB_GUI()
    gui.mainloop()