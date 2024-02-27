from tkinter import *
from math import *

root = Tk()
r = 25
cord = []

# Створюємо полотно
canvas = Canvas(root, width=800, height=800)
canvas.pack(side=LEFT)


def checkDist(cur):
    for el in cord:
        if (el[0] - cur[0]) ** 2 + (el[1] - cur[1]) ** 2 < 4 * (r + 5) ** 2:
            return False

    return True


def onCanvasClick(ev: Event):
    print(ev)

    if checkDist((ev.x, ev.y)):
        cord.append((ev.x, ev.y))
        canvas.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r)


canvas.bind('<Button-1>', onCanvasClick)

root.mainloop()
