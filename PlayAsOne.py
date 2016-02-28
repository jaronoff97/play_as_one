#! usr/bin/env python2

import pyautogui
import Tkinter as tk
import threading
import time
import ttk


class PlayAsOne:
    def __init__(self):
        self.gui = GUI(self)

        self.running = False

        self.gui.mainloop()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def get_mode(self):
        return self.gui.mode_combobox.get()

    def get_input_mode(self):
        return self.gui.input_mode_combobox.get()

    def find_game_window(self):
        constant_position = pyautogui.locateOnScreen(self.gui.screenshot)
        if not constant_position:
            return False
        return (
            constant_position[0] - self.gui.screen_size[0],
            constant_position[1] - self.gui.screen_size[1],
            constant_position[0] + constant_position[2] + self.gui.screen_size[2],
            constant_position[1] + constant_position[3] + self.gui.screen_size[3]
        )

    def select_game_window(self):
        position = self.find_game_window()
        if not position:
            return False
        return True

    def send_key(self, key):
        if not self.running:
            return
        if not self.select_game_window():
            pyautogui.alert(text='Could not find game window')
        pyautogui.press(key)

    def send_mouse_click(self, x, y, button):
        if not self.running:
            return
        if not self.select_game_window():
            pyautogui.alert(text='Could not find game window')
        pyautogui.click(x=x, y=y, button=button)


class GUI(tk.Tk):
    def __init__(self, server):
        tk.Tk.__init__(self)
        self.server = server

        self.mode_frame = tk.Frame()
        self.mode_frame.grid(row=0, column=0, sticky='w')
        self.mode_label = tk.Label(self.mode_frame, text='Mode: ')
        self.mode_label.grid(row=0, column=0)
        self.mode_combobox = ttk.Combobox(self.mode_frame, state='readonly', width=9, values=('Chaos', 'Democracy'))
        self.mode_combobox.set('Chaos')
        self.mode_combobox.grid(row=0, column=1)

        self.input_mode_frame = tk.Frame(self)
        self.input_mode_frame.grid(row=1, column=0, sticky='w')
        self.input_mode_label = tk.Label(self.input_mode_frame, text='Input Mode: ')
        self.input_mode_label.grid(row=0, column=0)
        self.input_mode_combobox = ttk.Combobox(
            self.input_mode_frame, state='readonly', width=13, values=('NES', 'SNES', 'Full Keyboard'))
        self.input_mode_combobox.set('Full Keyboard')
        self.input_mode_combobox.grid(row=0, column=1)

        self.screenshot = None
        self.screen_size = None
        self.screenshot_label = tk.Label(self, text='Screenshot Not Taken', font=('Helvetica', 15))
        self.screenshot_label.grid(row=2, column=0)
        self.screenshot_button = ttk.Button(self, text='Take Screenshot', command=self.take_screenshot)
        self.screenshot_button.grid(row=2, column=1)

        self.start_button = ttk.Button(self, text='Start', command=self.start)
        self.start_button.grid(row=3, column=0, columnspan=2)

        def s():
            print(self.server.find_game_window())
        self.k = ttk.Button(self, text='K', command=s)
        self.k.grid(row=4, column=0)

    def start(self):
        if self.screenshot is None:
            pyautogui.alert(text='You need to set a constant screenshot.', title='Screenshot', button='OK')
            return
        self.start_button.config(text='Stop', command=self.stop)
        self.server.start()

    def stop(self):
        self.start_button.config(text='Start', command=self.start)
        self.server.stop()

    def take_screenshot(self):
        def func():
            self.screenshot_button.config(state='disabled')

            for second in reversed(range(4)):
                self.screenshot_label.config(text='Deselect the game window %s' % second)
                if second != 0:
                    time.sleep(1)

            region = []
            for second in reversed(range(4)):
                self.screenshot_label.config(text='Place the mouse at the top left\nof the game\'s title bar %s' % second)
                if second != 0:
                    time.sleep(1)
            constant_top_left = pyautogui.position()
            region.extend(constant_top_left)
            for second in reversed(range(4)):
                self.screenshot_label.config(text='Place the mouse at the bottom right\nof the game\'s title bar %s' % second)
                if second != 0:
                    time.sleep(1)
            constant_bottom_right = pyautogui.position()
            region.extend(
                (constant_bottom_right[0] - constant_top_left[0], constant_bottom_right[1] - constant_top_left[1])
            )

            for second in reversed(range(4)):
                self.screenshot_label.config(text='Place mouse at the top left\nof the entire game window %s' % second)
                if second != 0:
                    time.sleep(1)
            top_left = pyautogui.position()
            for second in reversed(range(4)):
                self.screenshot_label.config(text='Place mouse at the bottom right\nof the entire game window %s' % second)
                if second != 0:
                    time.sleep(1)
            bottom_right = pyautogui.position()

            self.screen_size = [
                constant_top_left[0] - top_left[0],
                constant_top_left[1] - top_left[1],
                bottom_right[0] - constant_bottom_right[0],
                bottom_right[1] - constant_bottom_right[1]
            ]

            self.screenshot = pyautogui.screenshot(region=region)
            self.screenshot_taken = True
            self.screenshot_label.config(text='Screenshot Taken')
            self.screenshot_button.config(state='normal', text='Retake Screenshot')
        threading.Thread(target=func).start()
