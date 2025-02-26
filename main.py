import time
import tkinter as tk
import math
from tkinter import simpledialog
import pandas
from summary import show_pie_chart
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
reps = 1
timer = None
doTick = True
remaining_time = 0

dics = []

# ---------------------------- TIMER RESET ------------------------------- #
def load_data_base():
    global dics
    data = pandas.read_csv("Categories.csv")
    for index, row in data.iterrows():
        new_dics = {"category" : row["category"], "action": row["action"], "min" : int(row["min"])}
        dics.append(new_dics)

load_data_base()



def create_data_base():
    global dics
    data = pandas.DataFrame(dics)
    data.to_csv("Categories.csv")
def reset_time():
    global reps
    button1.config(state=tk.NORMAL)
    window.after_cancel(timer)
    reps = 1
    canvas.itemconfig(text_timer,text="00:00")
    text.config(text="TIMER", fg=GREEN)


def stop_timer():
    global doTick
    global remaining_time
    button1.config(state=tk.NORMAL)
    doTick = False
    remaining_time = int(canvas.itemcget(text_timer, 'text').split(':')[0]) * 60 + int(canvas.itemcget(text_timer, 'text').split(':')[1])
    print(remaining_time)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global remaining_time
    global reps
    global doTick
    doTick = True
    button1.config(state=tk.DISABLED)
    if remaining_time > 0:
        countdown(remaining_time)
        remaining_time = 0
    else:
        if reps == 1 or reps == 3 or reps == 5 or reps == 7:
            mark.config(text="")
            countdown(WORK_MIN * 60)
            text.config(text="WORK TIME", fg=RED)
            reps+=1
        elif reps == 2 or reps == 4 or reps == 6:
            countdown(SHORT_BREAK_MIN * 60)
            text.config(text="SHORT BREEAK", fg=GREEN)
            mark.config(text="✅")
            reps+=1

        elif reps == 8:
            countdown(LONG_BREAK_MIN * 60)
            mark.config(text="✅")
            text.config(text="LONG BREAAAK", fg=GREEN)





# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global dics
    minutes = math.floor(count / 60)
    sec = count % 60
    if sec == 0:
        sec = "00"
    if sec in range(1,10):
        sec = f"0{sec}"
    canvas.itemconfig(text_timer, text=f"{minutes}:{sec}")
    if not doTick:
        return
    if count > 0:
        global timer
        timer = window.after(100, countdown, count - 1)
    else:
        if count == 0:
            category = simpledialog.askstring("Input", "Please select your category\n-Leisure\n-Work\n-Cleaning\n-Cooking\n")
            action = simpledialog.askstring("Input", "Please input your action")
            min = simpledialog.askinteger("Input", "Please input your values in min")

            new_dics = {"category" : category, "action": action, "min" : min}
            dics.append(new_dics)
            create_data_base()
            start_timer()


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()

photo = tk.PhotoImage(file="tomato.png")
window.title("Pomodorro gay title")
window.minsize(300, 400)
window.config(bg=YELLOW, padx=100, pady=40)


text = tk.Label(text="Timer", font=(FONT_NAME, 30, "bold"), bg=YELLOW, fg=GREEN)
text.grid(row=0, column=1)

canvas = tk.Canvas(width=225, height=224)
canvas.config(bg=YELLOW)

canvas.create_image(113, 112, image=photo)
text_timer = canvas.create_text(115, 130, text="00:00", font=(FONT_NAME, 25, "bold"), fill="white")
canvas.grid(row=1, column=1)

button1 = tk.Button(text="Start", width=10, command=start_timer)
button1.grid(row=2, column=0)

button2 = tk.Button(text="Reset", width=10, command=reset_time)
button2.grid(row=2, column=2)

button3= tk.Button(text="Stop", width=10, command=stop_timer)
button3.grid(row=2, column=1)

button4 = tk.Button(text="Summary", width=10, command=show_pie_chart)
button4.grid(row=3, column=1)

mark = tk.Label(bg=YELLOW, fg=GREEN)
mark.grid(sticky=tk.N)

window.mainloop()
