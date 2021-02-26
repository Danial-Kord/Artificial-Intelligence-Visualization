#!/usr/bin/env python
# from manim import *
from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
from manimlib import GraphSystem

CIRCLE_RADIUS = 1.5


class graph_search(Scene):
    def construct(self):
        # grid = ScreenGrid()
        path = input("enter path : ")
        graph = GraphSystem.Graph(CIRCLE_RADIUS)
        graph.read_from_file(path)
        root = graph.root

        current_y_point = 3
        delta_x = 3
        root.set_pos(3,current_y_point)
        current_y_point-=CIRCLE_RADIUS*2 + 2
        start_x_point = root.x - delta_x
        for i in graph.map[root]:
            i.set_pos(start_x_point,current_y_point)
            self.add(i.graphics,root.graphics,Arrow([root.x,root.y,0],[start_x_point,i.y,0],stroke_width=1,buff=CIRCLE_RADIUS))
            start_x_point += CIRCLE_RADIUS*2
        # c1 = Circle()
        # c1.radius = CIRCLE_RADIUS
        # c1.move_to([0,0,0])
        # root = GraphSystem.Node("A")
        # graph = GraphSystem.Graph(root)
        # root.setPos(0,0)
        # newNode = GraphSystem.Node("B")
        # newNode.setPos(3,3)
        # graph.insert(newNode,root)
        # self.add(Arrow([root.x,root.y,0],[newNode.x,newNode.y,0],stroke_width=1,buff=c1.radius))
        # self.add(root.graphics,newNode.graphics)
        self.wait(3)