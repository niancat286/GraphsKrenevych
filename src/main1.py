from tkinter import *


root = Tk()
r = 25
numOfTop = 1
cord = []


canvas = Canvas(root, width=800, height=800)
canvas.pack(side=LEFT)


def checkDist(cur):
    for el in cord:
        if (el[0] - cur[0]) ** 2 + (el[1] - cur[1]) ** 2 < 4 * (r + 2) ** 2:
            return False

    return True


def onCanvasClick(ev: Event):
    global numOfTop
    print(ev)


    if checkDist((ev.x, ev.y)):
        cord.append((ev.x, ev.y))
        canvas.option_clear()
        for i in range(numOfTop):
            canvas.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r, fill = 'lime')
            canvas.create_text(ev.x, ev.y, text = str(i+1))

        numOfTop += 1


canvas.bind('<Button-1>', onCanvasClick)

root.mainloop()
