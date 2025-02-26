from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas



def show_pie_chart():
    df = pandas.read_csv("Categories.csv")

    leis = df[df.category == "Leisure"]
    sum_leis = leis["min"].sum()

    clean = df[df.category == "Cleaning"]
    sum_clean = clean["min"].sum()

    work = df[df.category == "Work"]
    sum_work = work["min"].sum()

    cook = df[df.category == "Cooking"]
    sum_cook = cook["min"].sum()
    print(sum_cook)



    labels = ['Cooking', 'Working', 'Cleaning', 'Leisure']
    sizes = [sum_cook, sum_work, sum_clean, sum_leis]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)


    filtered_data = [(label, size, color, exp) for label, size, color, exp in zip(labels, sizes, colors, explode) if
                     size > 0]
    filtered_labels, filtered_sizes, filtered_colors, filtered_explode = zip(*filtered_data)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(filtered_sizes, explode=filtered_explode, labels=filtered_labels, colors=filtered_colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    chart_window = tk.Toplevel()

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    canvas_label = tk.Canvas(chart_window, width=canvas_widget.winfo_reqwidth(), height=50)
    canvas_label.pack(side=tk.TOP)
    label = tk.Label(canvas_label, text="Tag Distribution", font=("Arial", 14))
    canvas_label.create_window(canvas_label.winfo_reqwidth() / 2, 25, window=label)

    list_frame = tk.Frame(chart_window)
    list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    for label, size, color in zip(filtered_labels, filtered_sizes, filtered_colors):
        item_label = tk.Label(list_frame, text=f"{label}: {size} minutes", font=("Arial",15), fg=color)
        item_label.pack(anchor='w')




    def close_window():
        chart_window.destroy()

    button_close = ttk.Button(master=chart_window, text="Close the window", command=close_window)
    button_close.pack(side=tk.BOTTOM)



