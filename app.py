# ---------------------------- IMPORTS ---------------------------------- #
import tkinter as tk
import pygame
from utility import get_path

# ---------------------------- CONSTANTS -------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 10
# SOUND = "./assets/alarm10.mp3"
SOUND = get_path('assets/alarm10.mp3')
# FILE = "assets/tomato.png"
FILE = get_path('assets/tomato.png')
START_SOUND = 10
STOP_SOUND = 0

# ---------------------------- Global Variables -------------------------- #
reps = 0
timer = None
glob_minute = 0
glob_second = 0
pygame.mixer.init()
pygame.mixer.music.load(SOUND)  # Loading File Into Mixer


# ---------------------------- TIMER RESET ------------------------------- #
def reset_btn_used():
    # global reps, timer, minute, second, is_reset
    global reps, timer, glob_minute, glob_second
    # Stop music
    pygame.mixer.music.stop()
    # Cancel timer
    if timer is not None:
        window.after_cancel(timer)
    # reset text and color
    timer_label.config(text="TIMER", fg=GREEN)
    canvas.itemconfig(canvas_text, text="00:00")
    check_label.config(text="")
    # reset values
    reps = 0
    timer = None
    glob_minute = 0
    glob_second = 0
    # Hide pause and stop
    reset_pause_stop()


def reset_pause_stop():
    # reset text
    pause_btn.config(text="pause")
    # Hide pause and stop
    pause_btn.grid_forget()
    stop_btn.grid_forget()


def set_pause_stop():
    # Un Hide pause and stop
    pause_btn.grid(row=4, column=0)
    stop_btn.grid(row=4, column=2)


def set_canvas_label():
    # Set minute and second as per repo and update label_text and color
    minute, second = update_timer_label()
    # update canvas_text
    update_canvas_text(minute, second)
    return minute, second


def check_play_sound(minute, second):
    # Playing SOUND In The Whole Device
    if minute == 0 and second == START_SOUND:
        pygame.mixer.music.play()
    # Stop Playing SOUND In The Whole Device
    elif minute == 0 and second == STOP_SOUND:
        pygame.mixer.music.stop()
    # Pause Playing SOUND In The Whole Device
    if sound_btn.get() == 0:
        pygame.mixer.music.pause()
    # Resume Playing SOUND In The Whole Device
    elif sound_btn.get() == 1:
        pygame.mixer.music.unpause()


def update_check_label():
    if reps % 2 == 0 and reps <= 7:
        check_tick = "✅" * (reps // 2 + 1)
        check_label.config(text=check_tick, bg=YELLOW)


def update_canvas_text(minute, second):
    sec_str = '0' if len(str(second)) == 1 else ''
    min_str = '0' if len(str(minute)) == 1 else ''
    string = f"{min_str}{minute}:{sec_str}{second}"
    canvas.itemconfig(canvas_text, text=string)


def update_timer_label():
    if reps > 7:
        return
    elif reps % 2 == 0:
        minute, second = WORK_MIN, 0
        # minute, second = 0, 3
        timer_text, timer_color = "WORK", GREEN
    elif reps % 7 == 0:
        minute, second = LONG_BREAK_MIN, 0
        # minute, second = 0, 3
        timer_text, timer_color = "BREAK", RED
    else:
        minute, second = SHORT_BREAK_MIN, 0
        # minute, second = 0, 3
        timer_text, timer_color = "BREAK", PINK
    timer_label.config(text=timer_text, fg=timer_color)
    return minute, second


# ---------------------------- TIMER MECHANISM --------------------------- #
# start btn
def start_btn_used():
    # if reps > 7 then do nothing
    if reps > 7:
        reset_pause_stop()
        return
    # stop
    stop_btn_used()
    # Un hide the pause and stop
    set_pause_stop()
    # Call the counter
    counter(glob_minute, glob_second)


# stop btn
def stop_btn_used():
    global glob_minute, glob_second
    # reset pause and stop
    reset_pause_stop()
    # Stop Playing SOUND In The Whole Device
    pygame.mixer.music.stop()
    # Cancel the timer
    if timer is not None:
        window.after_cancel(timer)
    # if reps > 7 then do nothing
    if reps > 7:
        return
    # set canvas text and label text & color
    minute, second = set_canvas_label()
    # update global minute and second
    glob_minute, glob_second = minute, second


# pause btn
def pause_btn_used():
    # Cancel the timer
    if timer is not None:
        window.after_cancel(timer)
    # if paused
    if pause_btn['text'] == "pause":
        # Pause the SOUND
        pygame.mixer.music.pause()
        # change to resume
        pause_btn.config(text="resume")
        print("pause", glob_minute, glob_second)
    else:
        # Check and Play Sound
        check_play_sound(glob_minute, glob_second)
        # change to pause
        pause_btn.config(text="pause")
        print("resume", glob_minute, glob_second)
        # call/ resume counter
        counter(glob_minute, glob_second)


# ---------------------------- COUNTDOWN MECHANISM ------------------------ #
def counter(minute, second):
    global reps, timer, glob_minute, glob_second
    glob_minute, glob_second = minute, second
    # print("counter is running!")
    if second == -1 and minute > 0:
        timer = window.after(1000, counter, minute - 1, 59)
    elif minute > 0 or second >= 0:
        update_canvas_text(minute, second)
        check_play_sound(minute, second)
        timer = window.after(1000, counter, minute, second - 1)
    else:
        # update the check_label
        update_check_label()
        reps += 1
        if reps > 7:
            reset_pause_stop()
            return
        if autostart_btn.get() == 1:
            start_btn_used()
        else:
            # set canvas text and label text & color
            set_canvas_label()
            # Hide pause and stop
            reset_pause_stop()
            return


# ---------------------------- UI SETUP ---------------------------------- #
# Window
window = tk.Tk()
window.title("Pomodoro")
# window.minsize(width=250, height=225)
window.config(padx=50, pady=25, bg=YELLOW)

# Label
timer_label = tk.Label(
    text="TIMER", 
    font=(FONT_NAME, 40, "normal"), 
    fg=GREEN, 
    bg=YELLOW, 
    width=5, 
    height=1
)
timer_label.grid(row=1, column=1)

# Canvas
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file=FILE)
canvas.create_image(100, 112, image=tomato_img)
canvas_text = canvas.create_text(
    100, 
    130, 
    text="00:00", 
    fill="white", 
    font=(FONT_NAME, 20, "bold")
)
canvas.grid(row=2, column=1)

# start button
start_btn = tk.Button(
    text="start", 
    command=start_btn_used, 
    font=(FONT_NAME, 15, "normal"), 
    width=7
)
start_btn.grid(row=0, column=0)

# reset button
reset_btn = tk.Button(
    text="reset", 
    command=reset_btn_used, 
    font=(FONT_NAME, 15, "normal")
)
reset_btn.grid(row=0, column=2)

# pause button
pause_btn = tk.Button(
    text="pause", 
    command=pause_btn_used, 
    font=(FONT_NAME, 15, "normal"), 
    width=7
)
pause_btn.grid_forget()

# stop button
stop_btn = tk.Button(
    text="stop", 
    command=stop_btn_used, 
    font=(FONT_NAME, 15, "normal")
)
pause_btn.grid_forget()

# autostart checkbutton
autostart_btn = tk.IntVar()
autostart_check_btn = tk.Checkbutton(
    text="auto start", 
    variable=autostart_btn, 
    bg=YELLOW, 
    font=(FONT_NAME, 15, "normal")
)
autostart_check_btn.grid(row=5, column=1)

# sound checkbutton
sound_btn = tk.IntVar()
sound_check_btn = tk.Checkbutton(
    text="sound", 
    variable=sound_btn, 
    bg=YELLOW, 
    font=(FONT_NAME, 15, "normal"), 
    pady=15
)
sound_check_btn.grid(row=4, column=1)

# Checkmark Label
check_label = tk.Label(text="", bg=YELLOW)
check_label.grid(row=0, column=1)

# ---------------------------- UI SETUP ------------------------------- #
# Keep window (so that window can listen to events)
window.mainloop()
