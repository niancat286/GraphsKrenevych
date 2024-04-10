from tkinter import *
from tkinter import filedialog
from threading import Thread, Event
from time import sleep

MAX_ELEMS = 50
r = 25


def init():
    global numOfTop, active_vertex, cord, graph, selected_vertex, selected_vertex_for_delete, visited, finished, b,e, que
    numOfTop = 0
    selected_vertex = None
    selected_vertex_for_delete = None
    active_vertex = [False] * MAX_ELEMS
    cord = [(0, 0, 0)] * MAX_ELEMS  #третя координата це імʼя вершини

    graph = []
    for c in range(MAX_ELEMS):
        graph.append([0] * MAX_ELEMS)

    visited = []
    finished = []

    b = 0
    e = 0
    que = [0]*MAX_ELEMS

def dist_to_vertex(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2) ** 0.5


def find_vertex(v):
    for i in range(MAX_ELEMS):
        if not active_vertex[i]:  # вершина неактивна
            continue
        el = cord[i]
        if dist_to_vertex(el, v) < 2 * (r + 2):
            return el, i
    return None, None


def update():
    canvas.delete('all')
    for i in range(MAX_ELEMS):
        if not active_vertex[i]:
            continue

        for j in range(MAX_ELEMS):
            if active_vertex[j] and graph[i][j] == 1:
                canvas.create_line(cord[i][0], cord[i][1], cord[j][0], cord[j][1])

    for i in range(MAX_ELEMS):
        if active_vertex[i]:
            if i in finished:
                color_var = 'red'
            elif i in visited:
                color_var = 'blue'
            else:
                color_var = 'lime'
            canvas.create_oval(cord[i][0] - r, cord[i][1] - r, cord[i][0] + r, cord[i][1] + r, fill=color_var)
            canvas.create_text(cord[i][0], cord[i][1], text=str(cord[i][2]))


def count_active_vertex():
    num = 0
    for i in range(MAX_ELEMS):
        if active_vertex[i]:
            num += 1
    return num


def count_edges():
    num = 0
    for i in range(MAX_ELEMS):
        for j in range(MAX_ELEMS):
            if active_vertex[i] and active_vertex[j] and graph[i][j] == 1:
                num += 1

    return num


def find_free_place():
    for i in range(MAX_ELEMS):
        if not active_vertex[i]:
            return i

    raise RuntimeError("Graph is overloaded")


def addVertex(x, y, n):
    global numOfTop
    i = find_free_place()
    numOfTop += 1
    cord[i] = (x, y, n)
    active_vertex[i] = True

    update()


def onCanvasClickLeft(ev: Event):
    global selected_vertex, active_vertex

    current_point = (ev.x, ev.y)
    vertex, index = find_vertex(current_point)
    if vertex is None:
        ##selected_vertex = current_point
        addVertex(ev.x, ev.y, numOfTop+1)

    else:  # пошук вершин для побудови ребра
        if selected_vertex is None:
            selected_vertex = vertex

        elif selected_vertex == vertex:
            selected_vertex = None

        elif selected_vertex is not None and vertex != selected_vertex:
            v, index2 = find_vertex(selected_vertex)
            if graph[index][index2] == 1:
                graph[index][index2] = 0
                graph[index2][index] = 0

            else:
                graph[index][index2] = 1
                graph[index2][index] = 1

            selected_vertex = None

        update()


def remove_extra_ribs():
    global graph
    for i in range(MAX_ELEMS):
        if not active_vertex[i]:
            for j in range(MAX_ELEMS):
                graph[i][j] = 0
                graph[j][i] = 0


def onCanvasClickRight(ev: Event):  # використано для видалення елементів з канви
    global selected_vertex_for_delete, cord, selected_vertex
    current_point = (ev.x, ev.y)
    vertex, index = find_vertex(current_point)
    if vertex is not None:
        selected_vertex = None
        if selected_vertex_for_delete is None:
            selected_vertex_for_delete = vertex
        v, index = find_vertex(selected_vertex_for_delete)
        active_vertex[index] = False
        remove_extra_ribs()
        selected_vertex_for_delete = None
        update()

def find_max_n(array):
    maxn = 0
    for i in range(numOfTop-1):
        if array[i][2] < array[i+1][2]:
            maxn = array[i+1][2]
    return maxn


def load_graph():
    global graph, numOfTop
    filetypes = [('text files', '.txt')]
    canvas.filename = filedialog.askopenfilename(filetypes=filetypes)

    init()

    with open(canvas.filename, "r") as file1:
        V, E, N = map(int, file1.readline().split())
        for v in range(V):
            x, y, n = map(int, file1.readline().split())
            addVertex(x, y, n)

        for e in range(E):
            i1, i2 = map(int, file1.readline().split())
            graph[i1 - 1][i2 - 1] = 1

    update()
    numOfTop = find_max_n(cord)


def save_graph():
    global cord, graph
    filetypes = [('text files', '.txt')]
    canvas.filename = filedialog.askopenfilename(filetypes=filetypes)

    V = count_active_vertex()
    E = count_edges()
    N = numOfTop
    with open(canvas.filename, "w") as file1:
        print(V, E, N, file=file1)

        for v in range(MAX_ELEMS):
            if active_vertex[v]:
                x = cord[v][0]
                y = cord[v][1]
                n = cord[v][2]
                print(x, y, n, file=file1)

        for e in range(MAX_ELEMS):
            if active_vertex[e]:
                for i in range(MAX_ELEMS):
                    if graph[e][i] == 1:
                        print(e + 1, i + 1, file=file1)


def close():
    canvas.quit()


def find_min_vertex():
    min_num = cord[0][2]
    for i in range(MAX_ELEMS):
        if not active_vertex[i]:
            continue
        el = cord[i][2]
        if el <= min_num:
            min_num = el
    return min_num-1

def dfs(start):
    global graph, visited, finished
    print(f'-> {start+1}')
    visited.append(start)
    update()
    sleep(1)
    for neigh in range(MAX_ELEMS):
        if (graph[start][neigh] == 1) and (neigh not in visited):
            dfs(neigh)
    print(f'<- {start+1}')
    finished.append(start)
    update()
    sleep(1)


def dfs_start():
    global visited, finished
    visited = []
    finished = []
    update()

    el = find_min_vertex()
    thread = Thread(target=dfs, args=(el,))
    thread.start()

    update()


def push(elem):
    global b, e, que
    que[e] = elem
    e += 1

def pop():
    global b, e, que
    elem = que[b]
    b += 1
    return elem

def empty():
    global b, e
    return b == e


def bfs_start():
    global visited, finished
    visited = []
    finished = []
    update()

    thread = Thread(target=bfs)
    thread.start()

    update()



def bfs():
    global graph, b, e, que, visited, finished
    visited = []
    finished = []

    b = 0
    e = 0
    que = [0] * MAX_ELEMS

    start = find_min_vertex()
    push(start)
    visited.append(start)

    while not empty():
        start = pop()
        finished.append(start)
        update()
        sleep(1)

        for neigh in range(MAX_ELEMS):
            if (graph[start][neigh] == 1) and (neigh not in visited):
                push(neigh)
                visited.append(neigh)
                update()
                sleep(1)



if __name__ == '__main__':
    init()

    root = Tk()
    canvas = Canvas(root, width=800, height=800)
    canvas.pack(side=LEFT)

    button_exp_file = Button(canvas, text='Load graph', command=load_graph)
    button_exp_file.place(x=10, y=10)

    button_save_file = Button(canvas, text='Save graph', command=save_graph)
    button_save_file.place(x=110, y=10)

    button_close_file = Button(canvas, text='Exit', command=close)
    button_close_file.place(x=725, y=10)

    button_search_file = Button(canvas, text='DFS', command=dfs_start)
    button_search_file.place(x=250, y=10)

    button_search_file = Button(canvas, text='BFS', command=bfs_start)
    button_search_file.place(x=325, y=10)

    canvas.bind('<Button-1>', onCanvasClickLeft)
    canvas.bind('<Button-2>', onCanvasClickRight)

    root.mainloop()
