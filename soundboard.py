#!/usr/bin/env python3

import simpleaudio as sa
from subprocess import call
from collections import namedtuple
from os import listdir
from os.path import join
from sys import exit


class Song(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.obj = sa.WaveObject.from_wave_file(path)

    def play(self):
        self.play_obj = self.obj.play()

    def stop(self):
        self.play_obj.stop()

    def __repr__(self):
        return self.name


class Menu:

    def __init__(self, options, currently_playing=[]):
        self.update(options, currently_playing)

    def draw(self):
        for index, e in enumerate(self.options):
            print("{}: {}".format(self.index_to_ascii(index), e))
        if len(self.options) > 0:
            print()
        for index, e in enumerate(self.currently_playing):
            print("{}: {}".format(self.index_to_ascii(index, '0'), e))
        if len(self.currently_playing) > 0:
            print()

    def update(self, options, currently_playing):
        self.options = options
        self.currently_playing = list(currently_playing)
        self.draw()

    def index_to_ascii(self, index, start='a'):
        return chr(index + ord(start))

    def ascii_to_index(self, a, start='a'):
        return ord(a) - ord(start)

    def run(self):
        call('clear')
        while True:
            self.draw()
            result = getChar()
            call('clear')
            ind = self.ascii_to_index(result)
            ind_cp = self.ascii_to_index(result, '0')
            if ind < len(self.options) and ind >= 0:
                return self.options[ind]
            elif ind_cp < len(self.currently_playing) and ind_cp >= 0:
                return self.currently_playing[ind_cp]


def getChar():
    try:
        # for Windows-based systems
        import msvcrt  # If successful, we are on Windows
        return msvcrt.getch()

    except ImportError:
        # for POSIX-based systems (with termios & tty support)
        import tty
        import sys
        import termios  # raises ImportError if unsupported

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        if answer == chr(3):
            exit()
        return answer


def get_ui_choice(current_dir, currently_playing):
    if current_dir == None:
        dirs = listdir('audio')
        return (join('audio', Menu(dirs, currently_playing).run()),
                currently_playing)
    else:
        files = []
        for name in listdir(current_dir):
            files.append(Song(name, join(current_dir, name)))
        song_menu = Menu(["Go back"] + files, currently_playing)
        song = song_menu.run()
        if song == 'Go back':
            return (None, currently_playing)
        else:
            if song in currently_playing:
                # stop playing the song
                currently_playing.remove(song)
                song.stop()
            else:
                # start playing the song
                currently_playing.add(song)
                song.play()
            return (current_dir, currently_playing)

if __name__ == '__main__':
    call('clear')
    current_dir = None
    currently_playing = set()
    while True:
        current_dir, currently_playing = \
            get_ui_choice(current_dir, currently_playing)
