#!/usr/bin/env python
from manim import *
# from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
import GraphSystem

scale = 0.5

LEFT_X_AREA = -4
RIGHT_X_AREA = 4

class graph_search(MovingCameraScene):
    def construct(self):
        # grid = ScreenGrid()
        camera = self.camera_frame
        # camera.set_width(12)

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file(path)
        graph.show_complete_graph(self,RIGHT_X_AREA,LEFT_X_AREA)
        # root = graph.root
        # radius = graph.root.visual_shape.radius

        # current_y_point = 3
        # delta_x = 0
        # if graph.branching_factors[1] > 1:
        #     delta_x = (RIGHT_X_AREA - LEFT_X_AREA) / (graph.branching_factors[1]-1)
        # root.set_pos(0,current_y_point)
        # current_y_point-=scale*2 + scale
        # start_x_point = LEFT_X_AREA
        # for i in graph.map[root]:
        #     i.set_pos(start_x_point,current_y_point)
        #     self.add(i.graphics,root.graphics,Arrow([root.x,root.y,0],[start_x_point,i.y,0],stroke_width=1,buff= i.scale))
        #     start_x_point += delta_x
        
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