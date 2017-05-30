#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lakj
"""

import sys
import random
import time
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
SHORT_PAUSE = 5*60
LONG_PAUSE = 15*60
FILENAME = "work_done"
SPEED = 1

#Testing purposes
#FILENAME = "test"
#SPEED = 0.01

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


def pause_handler(sig, frm):
    """ Ctrl+c handler """

    fancy_print("Paused", bld=True, col=GRN)
    input()


def stop_handler(sig, frm):
    """ Ctrl+\ handler """

    fancy_print("Stopped", bld=True, col=RED)
    main_menu()


def beep():
    """ Play a sound """
    aplay = subprocess.Popen(["aplay", "beep.wav"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    aplay.communicate()
    aplay.terminate()


def clear():
    """ Clear the terminal """
    clear_screen = subprocess.Popen(["clear"])
    clear_screen.communicate()


def tick(char="  "):
    """ Prints some fancy colors """
    cols = [RED, GRN, YEL, BLU, MAG, CYN]
    selected = random.choice(cols)
    fancy_print(char, bld=True, rev=True, col=selected)


def cycle(length):
    """ Fancy waiting """

    seconds = 0
    while True:
        time.sleep(SPEED)
        seconds += 1
        if seconds % 60 == 0:
            tick(str(seconds // 60).zfill(2))
        else:
            tick()
        if seconds == length:
            break


def pause():
    """ Performs a pause """

    global tomatoes

    if tomatoes % 4 == 0:
        fancy_print("\nNice long break :) Enjoy your 15 mins!\n", bld=True, col=GRN)
        cycle(LONG_PAUSE)
    else:
        fancy_print("\nNice! enjoy your 5 mins!\n", bld=True, col=GRN)
        cycle(SHORT_PAUSE)


def summary():
    """ Asks for a brief summary of the work done during the pomodoro """
    fancy_print("\n\nPlease write a brief summary of what you have done:\n", bld=True, col=YEL)
    with open(FILENAME, "a") as work_file:
        clock = time.strftime("%Y-%m-%d %H:%M")
        work = input()
        work_file.write("- {0}\n    {1}\n\n".format(clock, work))


def tomato():
    """ Performs a tomato """

    fancy_print("Pwndoro {0} started focus now! Press ctrl-c to pause it or ctrl+\ to stop it\n".format(tomatoes+1),
                bld=True, col=RED)
    cycle(TOMATO_LEN)


def session():
    """ Starts the session """

    global tomatoes

    while True:
        tomato()
        tomatoes = tomatoes + 1
        beep()

        summary()
        beep()

        pause()
        beep()

        clear()


def main_menu():
    """ Main menu """

    global tomatoes

    while True:
        fancy_print("\n\nAre you ready? Currently {0} Pwndoros done.\n".format(tomatoes),
                    bld=True, col=YEL)
        fancy_print("[1] Yes, let's start working!\n")
        fancy_print("[!1] Nope, enough for today...\n> ")
        choice = input()
        fancy_print("\n")
        if choice == "1":
            clear()
            session()
        else:
            fancy_print("Ok bye!!\n", bld=True, col=YEL)
            exit(0)


def welcome():
    """ Display welcome message """
    fancy_print(" "*35+"\n  ", bld=True, rev=True, col=GRN)
    fancy_print(" Welcome to the ", bld=True, col=GRN)
    fancy_print("Pwndoro ", bld=True, col=RED)
    fancy_print("timer. ", bld=True, col=GRN)
    fancy_print("  \n"+" "*35+"\n", bld=True, rev=True, col=GRN)


def main():
    """ Pwndoro """

    global tomatoes
    tomatoes = 0
    signal.signal(signal.SIGINT, pause_handler)
    signal.signal(signal.SIGQUIT, stop_handler)

    welcome()

    main_menu()


if __name__ == "__main__":
    main()
