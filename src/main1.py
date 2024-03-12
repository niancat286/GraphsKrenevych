from tkinter import *


root = Tk()
r = 25
numOfTop = 0
cord = []
connect = []
connectFlag = False

for с in range(50):
    connect.append([0]*50)


canvas = Canvas(root, width=800, height=800)
canvas.pack(side=LEFT)


def checkDist(cur):
    for el in cord:
        if (el[0] - cur[0]) ** 2 + (el[1] - cur[1]) ** 2 < 4 * (r + 2) ** 2:
            return False
    return True


def update_canv():
    canvas.delete('all')
    for el in connect:
        canvas.create_line(cord[el[0]][0], cord[el[0]][1], cord[el[1]][0], cord[el[1]][1])
    for i in range(numOfTop):
        canvas.create_oval(cord[i][0] - r, cord[i][1] - r, cord[i][0] + r, cord[i][1] + r, fill='lime')
        canvas.create_text(cord[i][0], cord[i][1], text=str(i))


def onCanvasClickRight(ev: Event): #буде використано для видалення
    global numOfTop
    print(ev)
    if checkDist((ev.x, ev.y)):
        update_canv()
        canvas.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r, fill = 'lime')
        canvas.create_text(ev.x, ev.y, text = str(numOfTop))
        numOfTop -= 1


def onCanvasClickLeft(ev: Event):
    global numOfTop, connectFlag
    i = -1
    j = -1

    if checkDist((ev.x, ev.y)):
        cord.append((ev.x, ev.y))
        update_canv()
        canvas.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r, fill = 'lime')
        canvas.create_text(ev.x, ev.y, text = str(numOfTop))
        connectFlag = False
        numOfTop += 1

    elif not checkDist((ev.x, ev.y)):
        if not connectFlag:
            for el in cord:
                i += 1
                if (el[0] - ev.x) ** 2 + (el[1] - ev.y) ** 2 < 4 * r ** 2:
                    connectFlag = True
                    break


        else:
            for el in cord:
                j += 1
                if (el[0] - ev.x) ** 2 + (el[1] - ev.y) ** 2 < 4 * r ** 2:
                    connectFlag = False
                    break


            if (connect[i][j] != 1) and (connect[j][i] != 1):
                canvas.create_line(cord[i][0], cord[i][1], cord[j][0], cord[j][1])
                connect[i][j] = 1
                connect[j][i] = 1






canvas.bind('<Button-1>', onCanvasClickLeft)

root.mainloop()
