from random import shuffle
import turtle

class Graph:
   
    def __init__(self, C: int, R: int):
        self._right = [[False] * R for _ in range(C-1)]
        self._up = [[False] * (R-1) for _ in range(C)]
       
    def cols(self):
        return len(self._up)
   
    def rows(self):
        return len(self._right[0])
       
    def has_right(self, c: int, r: int):
        return self._right[c][r]
   
    def set_right(self, c: int, r: int, v = True):
        self._right[c][r] = v
   
    def has_left(self, c: int, r: int):
        return self.has_right(c-1, r)
   
    def has_up(self, c: int, r: int):
        return self._up[c][r]
   
    def set_up(self, c: int, r: int, v = True):
        self._up[c][r] = True
   
    def has_down(self, c: int, r: int):
        return self.has_up(c, r-1)

    @staticmethod
    def _min_max(n1, n2):
        return min(n1, n2), max(n1, n2)
   
    def has_edge(self, v1, v2) -> bool:
        if v1[0] == v2[0]:
            l, u = Graph._min_max(v1[1], v2[1])
            if l != u-1 or l < 0 or u >= self.rows():
                return False
            return self._up[v1[0]][l]
        elif v1[1] == v2[1]:
            l, u = Graph._min_max(v1[0], v2[0])
            if l != u-1 or l < 0 or u >= self.cols():
                return False
            return self._right[l][v1[1]]
        else:
            return False
       
    def set_edge(self, v1, v2, v = True):
        if v1[0] == v2[0]:
            l, u = Graph._min_max(v1[1], v2[1])
            if l != u-1 or l < 0 or u >= self.rows():
                raise ValueError()
            self._up[v1[0]][l] = v
        elif v1[1] == v2[1]:
            l, u = Graph._min_max(v1[0], v2[0])
            if l != u-1 or l < 0 or u >= self.cols():
                raise ValueError()
            self._right[l][v1[1]] = v
        else:
            raise ValueError()
   
    def neighbours(self, vertex, visited = None):
        result = []
        c, r = vertex
        if 0 < c: result.append((c-1, r))
        if c+1 < self.cols(): result.append((c+1, r))
        if 0 < r: result.append((c, r-1))
        if r+1 < self.rows(): result.append((c, r+1))
        if visited is not None:
            result = [n for n in result if n not in visited]
        return result
       

def draw_line(v1, v2):
    turtle.penup()
    turtle.goto(v1[0]*50-500, v1[1]*50-300)
    turtle.pendown()
    turtle.goto(v2[0]*50-500, v2[1]*50-300)
   
def draw_graph(g: Graph):
    turtle.begin_poly()
    draw_line((0, 0), (g.cols(), 0))
    draw_line((0, g.rows()), (g.cols(), g.rows()))
    draw_line((0, 1), (0, g.rows()))
    draw_line((g.cols(), 0), (g.cols(), g.rows()-1))
    for r in range(g.rows()-1):
        for c in range(g.cols()):
            if not g.has_up(c, r):
                draw_line((c, r+1), (c+1, r+1))
    for c in range(g.cols()-1):
        for r in range(g.rows()):
            if not g.has_right(c, r):
                draw_line((c+1, r), (c+1, r+1))
    turtle.end_poly()

def DFS(g: Graph, vertex, visited: set):
    visited.add(vertex)
    ns = g.neighbours(vertex)
    shuffle(ns)
    for n in ns:
        if n not in visited:
            g.set_edge(vertex, n)
            DFS(g, n, visited)

def BFS(g: Graph, vertex):
    q = deque()
    visited = set()
    q.append(vertex)
    visited.add(vertex)
    while q:
        v = q.popleft()
        ns = g.neighbours(v, visited)
        shuffle(ns)
        for n in ns:
            g.set_edge(v, n)
            visited.add(n)
            q.append(n)

def randS(g: Graph, vertex):
    q = []
    visited = set()
    q.append(vertex)
    visited.add(vertex)
    while q:
        q_index = randrange(len(q))
        v = q[q_index]
        ns = g.neighbours(v, visited)
        if len(ns) <= 1:
            q[q_index] = q[-1]
            q.pop()
        if ns:
            n = choice(ns)
            g.set_edge(v, n)
            visited.add(n)
            q.append(n)
           

g = Graph(20, 15)
DFS(g, (0,0), set())
draw_graph(g)
turtle.done()
