from tkinter import *

root = Tk()
r = 25
numOfTop = 0
cord = []
graph = []
connectFlag = False

for c in range(50):
    graph.append([0] * 50)

canvas = Canvas(root, width=800, height=800)
canvas.pack(side=LEFT)


def dist(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2) ** 0.5


def find(v):
    for el in cord:
        if dist(el, v) < 2 * (r + 2):
            return el
    return None


def find_index(v):
    for index, el in enumerate(cord):
        if dist(el, v) < 2 * (r + 2):
            return index
    return None

def checkDist(cur):
    for el in cord:
        if dist(el, cur) < 2 * (r + 2):
            return False
    return True


def update_canv():
    canvas.delete('all')

    for i in range(50):
        for j in range(50):
            if graph[i][j] == 1:
                canvas.create_line(cord[i][0], cord[i][1], cord[j][0], cord[j][1])

    for i in range(numOfTop):
        canvas.create_oval(cord[i][0] - r, cord[i][1] - r, cord[i][0] + r, cord[i][1] + r, fill='lime')
        canvas.create_text(cord[i][0], cord[i][1], text=str(i + 1))


def addVertex(x, y):
    global numOfTop, cord
    cord.append((x, y))
    update_canv()
    canvas.create_oval(x - r, y - r, x + r, y + r, fill='lime')
    canvas.create_text(x, y, text=str(numOfTop + 1))
    numOfTop += 1


selected_vertex = None


def onCanvasClickLeft(ev: Event):
    global selected_vertex

    current_point = (ev.x, ev.y)
    vertex = find(current_point)
    if vertex is None:
        selected_vertex = current_point
        addVertex(ev.x, ev.y)

    else:  # пошук вершин для побудови ребра
        if selected_vertex is None:
            selected_vertex = vertex

        elif selected_vertex == vertex:
            selected_vertex = None

        elif selected_vertex is not None and vertex != selected_vertex:
            index1 = find_index(vertex)
            index2 = find_index(selected_vertex)
            graph[index1][index2] = 1
            graph[index2][index1] = 1
            selected_vertex = None
            update_canv()


selected_vertex_for_delete = None

def onCanvasClickRight(ev: Event):  # використано для видалення елементів з канви
    global numOfTop, selected_vertex_for_delete, cord

    current_point = (ev.x, ev.y)
    vertex = find(current_point)

    if vertex is not None:

        if selected_vertex_for_delete is None:
            selected_vertex_for_delete = vertex



        index = find_index(selected_vertex_for_delete)

        cord.pop(index)
        selected_vertex_for_delete = None
        numOfTop -= 1

        update_canv()


        #graph[index][]







canvas.bind('<Button-1>', onCanvasClickLeft)
canvas.bind('<Button-2>', onCanvasClickRight)

root.mainloop()
