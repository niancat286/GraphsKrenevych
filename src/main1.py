from tkinter import *

root = Tk()
r = 40

# Створюємо полотно
canvas = Canvas(root, width=400, height=300)
canvas.pack(side=LEFT)


def onCanvasClick(ev: Event):
    print(ev)

    canvas.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r)


canvas.bind('<Button-1>', onCanvasClick)

root.mainloop()
