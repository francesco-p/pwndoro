#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lakj
"""


import sys
import random
import time
from datetime import datetime
import subprocess
import signal



# Colors
RST = b'\x1B[0m'
RED = b'\x1B[31m'
GRN = b'\x1B[32m'
YEL = b'\x1B[33m'
BLU = b'\x1B[34m'
MAG = b'\x1B[35m'
CYN = b'\x1B[36m'
BLD = b'\x1B[1m'
REV = b'\x1B[7m'
WHT = b'\x1B[37m'

TOMATO_LEN = 60*25
SHO_PAUSE_LEN = 5*60
LON_PAUSE_LEN = 15*60
FILENAME = "work_done"

#Testing purposes
#TOMATO_LEN = 5
#SHO_PAUSE_LEN = 3
#LON_PAUSE_LEN = 4
#FILENAME = "test"



def signal_handler(sig, frm):
    """ Ctrl+c handler """
    fancy_print("Paused", bld=True, col=GRN)
    input()

def kill(sig, frm):
    """ Ctrl+\ handler """
    fancy_print("EXIT", bld=True, col=RED)
    exit(1)



def fancy_print(msg, rev=False, bld=False, col=RST):
    """ Prints some messages in a fancy style  """

    if col == RST:
        sys.stdout.buffer.write(msg.encode())
        sys.stdout.buffer.flush()
        return

    if rev:
        if bld:
            sys.stdout.buffer.write(REV + BLD + col + msg.encode() + RST)
        else:
            sys.stdout.buffer.write(REV + col + msg.encode() + RST)
    else:
        if bld:
            sys.stdout.buffer.write(BLD + col + msg.encode() + RST)
        else:
            sys.stdout.buffer.write(col + msg.encode() + RST)

    sys.stdout.buffer.flush()


def tick(n="  "):
    """ Prints some fancy colors """
    cols = [RED, GRN, YEL, BLU, MAG, CYN]
    selected = random.choice(cols)
    fancy_print(n, bld=True, rev=True, col=selected)

def pause():
    """ Performs a pause """

    global tomatoes

    if tomatoes % 5 == 0:
        fancy_print("\nNice long break :) Enjoy your 15 mins!\n", bld=True, col=YEL)
        seconds = 0
        while True:
            tick()
            time.sleep(0.02)
            seconds += 1
            if seconds % 60 == 0:
                fancy_print(str(seconds // 60).zfill(2), rev=True, col=YEL, bld=True)
            if seconds == LON_PAUSE_LEN:
                break
    else:
        fancy_print("\nNice! enjoy your 5 mins!\n", bld=True, col=GRN)
        seconds = 0
        while True:
            tick()
            time.sleep(0.02)
            seconds += 1
            if seconds % 60 == 0:
                fancy_print(str(seconds // 60).zfill(2), rev=True, col=YEL, bld=True)
            if seconds == SHO_PAUSE_LEN:
                break
    
def beep():
    """ Play a sound """
    aplay = subprocess.Popen(["aplay", "beep.wav"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    aplay.communicate()
    aplay.terminate()

def clear():
    clear = subprocess.Popen(["clear"])
    clear.communicate()

def tomato():
    """ Performs a tomato """

    global tomatoes
    tomatoes = 1

    fancy_print("Pwndoro {0} started focus now! Press ctrl-c to pause it\n".format(tomatoes), bld=True, col=RED)
    seconds = 0
    while True:
        tick()
        time.sleep(0.01)
        seconds += 1
        if seconds % 60 == 0:
            fancy_print(str(seconds // 60).zfill(2), rev=True, col=YEL, bld=True)

        if seconds == TOMATO_LEN:
            beep()
            tomatoes = tomatoes + 1
            fancy_print("\n\nPlease write a brief summary of what you have done:\n", bld=True, col=YEL)
            with open(FILENAME, "a") as f:
                clock = time.strftime("%Y-%m-%d %H:%M")
                work = input()
                f.write("- {0}\n    {1}\n\n".format(clock, work))
            pause()
            clear()
            fancy_print("Pomodoro {0} started focus now!\n".format(tomatoes), bld=True, col=RED)
            beep()
            seconds = 0


def main_menu():
    """ Main menu """

    while True:
        fancy_print("Are you ready?\n", bld=True, col=YEL)
        fancy_print("[1] Yes, let's start working\n> ")
        choice = input()
        fancy_print("\n")
        if choice == "1":
            clear()
            tomato()
        else:
            break


def main():
    """ Pomodoro """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, kill)

    fancy_print(" "*35+"\n  ", bld=True, rev=True, col=GRN)
    fancy_print(" Welcome to the ", bld=True, col=GRN)
    fancy_print("Pwndoro ", bld=True, col=RED)
    fancy_print("timer. ", bld=True, col=GRN)
    fancy_print("  \n"+" "*35+"\n\n\n", bld=True, rev=True, col=GRN)

    main_menu()

    return 1

if __name__ == "__main__":
    main()
