#! usr/bin/env python2

import pyautogui
import Tkinter as tk
import ttk


class PlayAsOne:
    def __init__(self):
        self.gui = GUI()
        self.gui.mainloop()

    def take_game_screenshot(self):
        pass

    def find_game_window(self):
        pass

    def send_key(self, key):
        pass

    def send_mouse_click(self, x, y, button):
        pass


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.mode_frame = tk.Frame()
        self.mode_frame.grid(row=0, column=0)

        self.mode_label = tk.Label(self.mode_frame, text='Mode: ')
        self.mode_label.grid(row=0, column=0)

        self.mode_combobox = ttk.Combobox(self.mode_frame, state='readonly', width=9, values=('Chaos', 'Democracy'))
        self.mode_combobox.grid(row=0, column=1)
