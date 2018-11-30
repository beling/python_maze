#!/usr/bin/env python3
import turtle
import sys
from random import randint

class SVGDrawer:
    
    CELL_SIZE = 20
    
    def __init__(self, file):
        self.file = file
        self.file.write("""<?xml version="1.0" encoding="UTF-8" ?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
""")
    
    @staticmethod
    def init_rect(width, height):
        return Rectangle(Point(1, 1), Point(1+width, 1+height))
        
    def close(self):
        self.file.write("</svg>")
    
    def goto(self, point):
        self.point = point

    def drawto(self, point):
        self.file.write(
            '<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:rgb(0,0,0)"/>'.format(
                self.point.x*self.CELL_SIZE, self.point.y*self.CELL_SIZE, point.x*self.CELL_SIZE, point.y*self.CELL_SIZE)
        )
        self.goto(point)
        

class TurtleDrawer:
    
    CELL_SIZE = 20
    
    def __init__(self):
        turtle.color('black')
        turtle.begin_poly()
        
    @staticmethod
    def init_rect(width, height):
        hw, hh = width//2, height//2
        return Rectangle(Point(-hw, -hh), Point(width-hw, height-hh))
        
    def close(self):
        turtle.end_poly()
        turtle.done()
    
    def goto(self, point):
        turtle.penup()
        turtle.goto(point.x*self.CELL_SIZE, point.y*self.CELL_SIZE)
    
    def drawto(self, point):
        turtle.pendown()
        turtle.goto(point.x*self.CELL_SIZE, point.y*self.CELL_SIZE)
    

class Point:
    """2D point"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def translated(self, dx=0, dy=0):
        """return new point equals to self translated by dx, dy"""
        return Point(self.x+dx, self.y+dy)

class Line:
    
    def __init__(self, begin_point: Point, length: int, is_horizontal: bool):
        self.begin_point = begin_point
        self.length = length
        self.is_horizontal = is_horizontal
        
    def point_on_line(self, delta: int):
        if self.is_horizontal:
            return self.begin_point.translated(dx=delta)
        else:
            return self.begin_point.translated(dy=delta)
        #return self.begin_point.translated(dx=delta) if self.is_horizontal else self.begin_point.translated(dy=delta)
        
    @property
    def end_point(self):
        return self.point_on_line(self.length)
        
    def draw(self, drawer):
        drawer.goto(self.begin_point)
        drawer.drawto(self.end_point)
        
    def draw_with_hole(self, drawer, hole_pos = None):
        if hole_pos is None:
            hole_pos = randint(0, self.length-1)
        elif hole_pos < 0:
            hole_pos += self.length
        drawer.goto(self.begin_point)
        drawer.drawto(self.point_on_line(hole_pos))
        drawer.goto(self.point_on_line(hole_pos+1))
        drawer.drawto(self.end_point)

class Rectangle:
    
    def __init__(self, lo, up):
        self.lo = lo
        self.up = up
        
    @property
    def width(self):
        return self.up.x - self.lo.x
    
    @property
    def height(self):
        return self.up.y - self.lo.y
    
    def horizontal_line(self, delta):
        return Line(self.lo.translated(dy=delta), self.width, True)
    
    def vertical_line(self, delta):
        return Line(self.lo.translated(dx=delta), self.height, False)
    
    def draw_with_holes(self, drawer):
        self.horizontal_line(0).draw(drawer)
        self.vertical_line(self.width).draw_with_hole(drawer, -1)
        self.vertical_line(0).draw_with_hole(drawer, 0)
        self.horizontal_line(self.height).draw(drawer)
        
    def rand_split_line(self):
        r = randint(1, self.width + self.height - 2)
        if r < self.width:
            return self.vertical_line(r)
        else:
            return self.horizontal_line(r-self.width+1)
        
    def split(self, line: Line):
        return Rectangle(self.lo, line.end_point),\
                Rectangle(line.begin_point, self.up)
    
    def draw_inside(self, drawer):
        if self.width <= 1 or self.height <= 1:
            return
        line = self.rand_split_line()
        line.draw_with_hole(drawer)
        for r in self.split(line):
            r.draw_inside(drawer)

def run(drawer, w = 20, h = 15):
    r = drawer.init_rect(w, h)
    r.draw_with_holes(drawer)
    r.draw_inside(drawer)
    drawer.close()


if __name__ == "__main__":
    try:
        if sys.argv[1] == 'svg':
            with open("out.svg", "w") as f:
                run(SVGDrawer(f))
        elif sys.argv[1] == 'www':
            from flask import Flask, Response
            from io import StringIO
            app = Flask(__name__)
            
            @app.route('/<int:w>/<int:h>')
            def with_size(w, h):
                with StringIO() as f:
                    run(SVGDrawer(f), w, h)
                    return Response(f.getvalue(), mimetype="image/svg+xml")
            
            @app.route('/')
            def default_size():
                return with_size(30, 20)
            
            app.run()
        else:
            run(TurtleDrawer())
    except IndexError:
        run(TurtleDrawer())
