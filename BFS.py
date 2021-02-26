#!/usr/bin/env python
import copy
from manim import *
# from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
import GraphSystem

scale = 0.5





class graph_search(MovingCameraScene):
    def construct(self):
        LEFT_X_AREA = -4
        RIGHT_X_AREA = 4
        # grid = ScreenGrid()
        camera = self.camera_frame
        # camera.set_width(12)

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,RIGHT_X_AREA,LEFT_X_AREA)
        self.play(sample_graph.animate.scale(0.5))
        self.wait(1)
        self.play(sample_graph.animate.to_edge(UL))
        self.wait(1)
        self.play(Write(Line([0,20,0],[0,-20,0]).next_to(sample_graph)))


        # Start BFS
        clone_graph = copy.deepcopy(graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = sample_graph.get_width() + sample_graph.get_center()[0] + 0.5
        RIGHT_X_AREA = 5.5
        self.play(draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
        draw_root.set_color(BLUE_A)
        self.play(draw_root.animate.scale(1.5))

        frontier = []
        explored = []
        way = []
        frontier.append(clone_graph.root)
        while(True):
            if len(frontier) == 0:
                break
            expand_node = frontier.pop()
            explored.append(expand_node)
            if clone_graph.map.__contains__(expand_node):
                for i in clone_graph.map[expand_node]:
                    if i in explored:
                        continue
                    frontier.append(i)
                    draw_root = i.graphics
                    pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                    self.play(draw_root.animate.move_to(pos))
                    draw_root.set_color(BLUE_A)
                    arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=1,buff=draw_root.get_width()*1.5/2,color=YELLOW)
                    i.set_dad(expand_node,arrow)
                    
                    self.play(Write(arrow),draw_root.animate.scale(1.5))

                    if i.name == "G":
                        temp = i
                        while temp.dad is not None:
                            way.append(temp)
                            temp = temp.dad
                        way.append(temp)
                        way.reverse()
                        for j in way:
                            if j.arrow is not None:
                                arrow = j.arrow
                                arrow.set_color(GREEN)
                                self.play(Write(arrow))
                                j.graphics.set_color(GREEN)
                                self.add(j.graphics)
                                self.wait(0.5)
                            else:
                                j.graphics.set_color(GREEN)
                                self.play(Write(j.graphics))
                        break

                    
        v = VGroup

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