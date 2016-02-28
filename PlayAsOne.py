#! usr/bin/env python2

import pyautogui
import Tkinter as tk
import ttk
import sys
if sys.platform == 'win32':
    import win32gui
if sys.platform == 'darwin':
    pass


class PlayAsOne:
    def __init__(self):
        self.gui = GUI(self)

        self.running = False

        self.gui.mainloop()

    def start(self):
        if not self.find_game_window():
            self.gui.status_label.config(text='Could not locate the window!')

        self.running = True
        self.gui.start_button.config(text='Stop', command=self.stop)
        self.gui.status_label.config(text='Running')
        self.gui.titlebar_entry.config(state='disabled')

    def stop(self):
        self.gui.start_button.config(text='Start', command=self.start)
        self.gui.status_label.config(text='Not Running')
        self.gui.titlebar_entry.config(state='normal')
        self.running = False

    def is_running(self):
        return self.running

    def get_mode(self):
        return self.gui.mode_combobox.get()

    def get_input_mode(self):
        return self.gui.input_mode_combobox.get()

    def find_game_window(self):
        if sys.platform == 'win32':
            toplist, winlist = [], []

            def enum_cb(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
            win32gui.EnumWindows(enum_cb, toplist)

            window = [(hwnd, title) for hwnd, title in winlist if self.gui.titlebar_entry.get().lower() in title.lower()]
            if not window:
                return False
            window = window[0]
            hwnd = window[0]

            win32gui.SetForegroundWindow(hwnd)
            region = win32gui.GetWindowRect(hwnd)
            region = (
                region[0],
                region[1],
                region[2]-region[0],
                region[3]-region[1]
            )
            return region
        return False

    def send_key(self, key):
        if not self.running:
            return
        self.find_game_window()
        pyautogui.press(key)

    def send_mouse_click(self, x, y, button):
        if not self.running:
            return
        window_region = self.find_game_window()
        if x < window_region[0]:
            return
        if y < window_region[1]:
            return
        if x > window_region[2]:
            return
        if y > window_region[2]:
            return
        pyautogui.click(x=x, y=y, button=button)


class GUI(tk.Tk):
    def __init__(self, server):
        tk.Tk.__init__(self)
        self.server = server

        self.mode_frame = tk.Frame(self)
        self.mode_frame.grid(row=0, column=0, columnspan=2)

        self.mode_label = tk.Label(self.mode_frame, text='Mode: ')
        self.mode_label.grid(row=0, column=0, sticky='w')
        self.mode_combobox = ttk.Combobox(self.mode_frame, state='readonly', width=9, values=('Chaos', 'Democracy'))
        self.mode_combobox.set('Chaos')
        self.mode_combobox.grid(row=0, column=1, sticky='ew')

        self.input_mode_label = tk.Label(self.mode_frame, text='Input Mode: ')
        self.input_mode_label.grid(row=1, column=0, sticky='w')
        self.input_mode_combobox = ttk.Combobox(
            self.mode_frame, state='readonly', width=13, values=('NES', 'SNES', 'Full Keyboard'))
        self.input_mode_combobox.set('Full Keyboard')
        self.input_mode_combobox.grid(row=1, column=1, sticky='ew')

        self.titlebar_label = tk.Label(self.mode_frame, text='Title Bar Name: ')
        self.titlebar_label.grid(row=2, column=0, sticky='w')
        self.titlebar_entry = ttk.Entry(self.mode_frame)
        self.titlebar_entry.grid(row=2, column=1, sticky='ew')

        self.status_label = tk.Label(self, text='Not Running')
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.start_button = ttk.Button(self, text='Start', command=self.server.start)
        self.start_button.grid(row=4, column=0, columnspan=2)
