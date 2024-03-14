from tkinter import *
from tkinter import filedialog

root = Tk()
r = 25
numOfTop = 0
numOfRibs = 0
cord = []
graph = []
active_vertex = []

for c in range(50):
    graph.append([0] * 50)

for c in range(50):
    active_vertex.append(1)

canvas = Canvas(root, width=800, height=800)
canvas.pack(side=LEFT)


def dist_to_vertex(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2) ** 0.5


def find_vertex(v):
    for el in cord:
        if dist_to_vertex(el, v) < 2 * (r + 2):
            return el
    return None


def find_index(v):
    for index, el in enumerate(cord):
        if dist_to_vertex(el, v) < 2 * (r + 2):
            return index
    return None


def checkDist(cur):
    for el in cord:
        if dist_to_vertex(el, cur) < 2 * (r + 2):
            return False
    return True


def update_canv():
    global numOfRibs
    numOfRibs = 0
    canvas.delete('all')
    vertex_num = 1
    for i in range(numOfTop):
        for j in range(numOfTop):
            if graph[i][j] == 1 and active_vertex[i] == 1 and active_vertex[j] == 1:
                canvas.create_line(cord[i][0], cord[i][1], cord[j][0], cord[j][1])
                numOfRibs += 1

    for i in range(numOfTop):
        if active_vertex[i] == 1:
            canvas.create_oval(cord[i][0] - r, cord[i][1] - r, cord[i][0] + r, cord[i][1] + r, fill='lime')
            canvas.create_text(cord[i][0], cord[i][1], text=str(vertex_num))
            vertex_num += 1


def count_active_vertex():
    num = 0
    for i in range(numOfTop):
        if active_vertex[i] == 1:
            num += 1
    return num


def addVertex(x, y):
    global numOfTop, cord
    cord.append((x, y))
    update_canv()
    canvas.create_oval(x - r, y - r, x + r, y + r, fill='lime')
    canvas.create_text(x, y, text=str(count_active_vertex() + 1))
    numOfTop += 1


selected_vertex = None


def onCanvasClickLeft(ev: Event):
    global selected_vertex, active_vertex, numOfRibs

    current_point = (ev.x, ev.y)
    vertex = find_vertex(current_point)
    if vertex is None:
        selected_vertex = current_point
        addVertex(ev.x, ev.y)

    elif active_vertex[find_index(vertex)] == 0:
        selected_vertex = current_point
        active_vertex[find_index(vertex)] = 1
        update_canv()


    else:  # пошук вершин для побудови ребра
        if selected_vertex is None:
            selected_vertex = vertex

        elif selected_vertex == vertex:
            selected_vertex = None

        elif selected_vertex is not None and vertex != selected_vertex:
            index1 = find_index(vertex)
            index2 = find_index(selected_vertex)
            if graph[index1][index2] == 1:
                graph[index1][index2] = 0
                graph[index2][index1] = 0
                numOfRibs -= 1

            else:
                graph[index1][index2] = 1
                graph[index2][index1] = 1


            selected_vertex = None
            update_canv()


selected_vertex_for_delete = None


def remove_extra_ribs():
    global graph, numOfRibs
    for i in range(50):
        if active_vertex[i] == 0:
            for j in range(50):
                graph[i][j] = 0
                graph[j][i] = 0
                numOfRibs -= 1


def onCanvasClickRight(ev: Event):  # використано для видалення елементів з канви
    global numOfTop, selected_vertex_for_delete, cord, selected_vertex
    current_point = (ev.x, ev.y)
    vertex = find_vertex(current_point)
    if vertex is not None:
        selected_vertex = None
        if selected_vertex_for_delete is None:
            selected_vertex_for_delete = vertex
        index = find_index(selected_vertex_for_delete)
        active_vertex[index] = 0
        remove_extra_ribs()
        selected_vertex_for_delete = None
        update_canv()


def graph_from_file():
    global cord, graph, numOfTop, numOfRibs, selected_vertex, selected_vertex_for_delete
    filetypes = [('text files', '.txt')]
    canvas.filename = filedialog.askopenfilename(filetypes=filetypes)

    for i in range(50):
        for j in range(50):
            graph[i][j] = 0

    cord = []
    numOfTop = 0
    numOfRibs = 0
    selected_vertex = None
    selected_vertex_for_delete = None
    for c in range(50):
        active_vertex[c] = 1

    with open(canvas.filename, "r") as file1:
        V, E = map(int, file1.readline().split())
        for v in range(V):
            x, y = map(int, file1.readline().split())
            cord.append((x, y))

        for e in range(E):
            i1, i2 = map(int, file1.readline().split())
            graph[i1 - 1][i2 - 1] = 1
            graph[i2 - 1][i1 - 1] = 1

    numOfTop = V
    numOfRibs = E
    update_canv()


def graph_in_file():
    global cord, graph, numOfTop, numOfRibs
    filetypes = [('text files', '.txt')]
    canvas.filename = filedialog.askopenfilename(filetypes=filetypes)
    with open(canvas.filename, "w") as file1:
        V = str(count_active_vertex())
        E = str(numOfRibs)
        file1.write(V)
        file1.write(' ')
        file1.write(E)
        file1.write('\n')
        for v in range(numOfTop):
            if active_vertex[v] == 1:
                x = str(cord[v][0])
                y = str(cord[v][1])
                file1.write(x)
                file1.write(' ')
                file1.write(y)
                file1.write('\n')

        for e in range(numOfTop):
            if active_vertex[e] == 1:
                for i in range(numOfTop):
                    if graph[e][i] == 1:
                        i1 = str(e + 1)
                        i2 = str(i + 1)
                        file1.write(i1)
                        file1.write(' ')
                        file1.write(i2)
                        file1.write('\n')


def close():
    canvas.quit()


button_exp_file = Button(canvas, text='Export file', command=graph_from_file)
button_exp_file.place(x=10, y=10)

button_save_file = Button(canvas, text='Save graph', command=graph_in_file)
button_save_file.place(x=110, y=10)

button_close_file = Button(canvas, text='Exit', command=close)
button_close_file.place(x=725, y=10)

canvas.bind('<Button-1>', onCanvasClickLeft)
canvas.bind('<Button-2>', onCanvasClickRight)

root.mainloop()
