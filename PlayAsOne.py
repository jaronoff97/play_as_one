#! usr/bin/env python2

import pyautogui
import Tkinter as tk
import threading
import time
import ttk
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify
from flask.ext.socketio import SocketIO, emit
from json import loads, dumps

class PlayAsOne:

    def __init__(self):
        self.gui = GUI(self)

        self.running = False
        self.window_active = False
        self.window_region = None

        threading.Thread(target=socketio.run, args=(app,)).start()
        self.gui.mainloop()

    def start(self):
        self.running = True
        self.gui.status_label.config(text='Running')
        threading.Thread(target=self.monitor_game_window).start()

    def stop(self):
        self.gui.status_label.config(text='Not Running')
        self.running = False

    def is_running(self):
        return self.running

    def get_mode(self):
        return self.gui.mode_combobox.get()

    def get_input_mode(self):
        return self.gui.input_mode_combobox.get()

    def monitor_game_window(self):
        while self.running:
            region = self.find_game_window()
            if not region:
                self.gui.stop()
                self.window_active = False
                self.window_region = None
                self.gui.status_label.config(text='Lost the game window!')
                break
            self.window_active = True
            self.window_region = region

            print(self.window_region)

            time.sleep(1)

    def find_game_window(self):
        position = pyautogui.locateOnScreen(self.gui.selected_screenshot)
        if not position:
            position = pyautogui.locateOnScreen(self.gui.deselected_screenshot)
        if not position:
            return False
        pyautogui.click(*pyautogui.center(position), button='left')
        return (
            position[0] - self.gui.screen_size[0],
            position[1] - self.gui.screen_size[1],
            position[0] + position[2] + self.gui.screen_size[2],
            position[1] + position[3] + self.gui.screen_size[3]
        )

    def send_key(self, key):
        if not self.running:
            return
        pyautogui.press(key)

    def send_mouse_click(self, x, y, button):
        if not self.running:
            return
        if x < self.window_region[0]:
            return
        if y < self.window_region[1]:
            return
        if x > self.window_region[2]:
            return
        if y > self.window_region[2]:
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
        self.mode_combobox = ttk.Combobox(
            self.mode_frame, state='readonly', width=9, values=('Chaos', 'Democracy'))
        self.mode_combobox.set('Chaos')
        self.mode_combobox.grid(row=0, column=1, sticky='ew')

        self.input_mode_label = tk.Label(self.mode_frame, text='Input Mode: ')
        self.input_mode_label.grid(row=1, column=0, sticky='w')
        self.input_mode_combobox = ttk.Combobox(
            self.mode_frame, state='readonly', width=13, values=('NES', 'SNES', 'Full Keyboard'))
        self.input_mode_combobox.set('Full Keyboard')
        self.input_mode_combobox.grid(row=1, column=1, sticky='ew')

        self.deselected_screenshot = None
        self.selected_screenshot = None
        self.screen_size = None
        self.screenshot_label = tk.Label(
            self, text='Screenshot Not Taken', font=('Helvetica', 15))
        self.screenshot_label.grid(row=2, column=0)
        self.screenshot_button = ttk.Button(
            self, text='Take Screenshot', command=self.take_screenshot)
        self.screenshot_button.grid(row=2, column=1)

        self.status_label = tk.Label(self, text='Not Running')
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.start_button = ttk.Button(self, text='Start', command=self.start)
        self.start_button.grid(row=4, column=0, columnspan=2)

    def start(self):
        if self.deselected_screenshot is None:
            pyautogui.alert(
                text='You need to set a constant screenshot.', title='Screenshot', button='OK')
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
                self.screenshot_label.config(
                    text='Deselect the game window %s' % second)
                if second != 0:
                    time.sleep(1)

            region = []
            for second in reversed(range(4)):
                self.screenshot_label.config(
                    text='Place the mouse at the top left\nof the game\'s title bar %s' % second)
                if second != 0:
                    time.sleep(1)
            constant_top_left = pyautogui.position()
            region.extend(constant_top_left)
            for second in reversed(range(4)):
                self.screenshot_label.config(
                    text='Place the mouse at the bottom right\nof the game\'s title bar %s' % second)
                if second != 0:
                    time.sleep(1)
            constant_bottom_right = pyautogui.position()
            region.extend(
                (constant_bottom_right[0] - constant_top_left[0],
                 constant_bottom_right[1] - constant_top_left[1])
            )
            self.deselected_screenshot = pyautogui.screenshot(region=region)
            pyautogui.click()
            self.selected_screenshot = pyautogui.screenshot(region=region)

            for second in reversed(range(4)):
                self.screenshot_label.config(
                    text='Place mouse at the top left\nof the entire game window %s' % second)
                if second != 0:
                    time.sleep(1)
            top_left = pyautogui.position()
            for second in reversed(range(4)):
                self.screenshot_label.config(
                    text='Place mouse at the bottom right\nof the entire game window %s' % second)
                if second != 0:
                    time.sleep(1)
            bottom_right = pyautogui.position()

            self.screen_size = [
                constant_top_left[0] - top_left[0],
                constant_top_left[1] - top_left[1],
                bottom_right[0] - constant_bottom_right[0],
                bottom_right[1] - constant_bottom_right[1]
            ]

            self.screenshot_taken = True
            self.screenshot_label.config(text='Screenshot Taken')
            self.screenshot_button.config(
                state='normal', text='Retake Screenshot')
        threading.Thread(target=func).start()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
user_count = 0
users = {}
democracy = []


@app.route("/")
def hello():
    print("User entered")
    return render_template('index.html')


@socketio.on('connect', namespace="/")
def test_connect():
    print('test ran')


@socketio.on("add user", namespace="/")
def handle_add_user(username):
    global user_count
    user_count += 1
    user = username
    print user
    users[user] = {'input_count': 0}
    emit("initialize", {
         'input_type': gui_server.get_input_mode(), 'mode': gui_server.get_mode()})


def handle_chaos(user_input):
    gui_server.execute_input(user_input)


def handle_democracy(user_input):
    global democracy
    for demo_input in democracy:
        if demo_input[0] == user_input['input']:
            demo_input[1] += 1
            break
    democracy.append((user_input['input'], 1))


def execute_democracy():
    most_votes = ("", 0)
    for user_input in democracy:
        if user_input[1] > most_votes[1]:
            most_votes = user_input
    gui_server.execute_input(most_votes[0])


@socketio.on('on disconnect', namespace="/")
def handle_disconnect(json):
    global user_count
    user_count -= 1
    user = loads(json)
    users.pop(user['username'])


@socketio.on("sendInput", namespace="/")
def handle_input(json):
    user_input = loads(json)
    users[input['username']]['input_count'] += 1
    if (gui_server.get_mode() == 'Chaos'):
        handle_chaos(user_input)
    elif (gui_server.get_mode() == 'Democracy'):
        handle_democracy(user_input)

if __name__ == '__main__':
    gui_server = PlayAsOne()
