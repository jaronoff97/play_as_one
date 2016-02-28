#! usr/bin/env python2

import pyautogui
import Tkinter as tk
import ttk


class PlayAsOne:
    def __init__(self):
        self.gui = GUI()
        self.gui.mainloop()

    def find_game_window(self):
        pass

    def send_key(self, key):
        pass

    def send_mouse_click(self, x, y, button):
        pass


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
