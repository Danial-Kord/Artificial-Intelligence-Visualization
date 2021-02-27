#!/usr/bin/env python
import copy
from operator import le
from manim import *
# from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
import GraphSystem

scale = 0.5




between_Text_gaps = 0.5

class graph_search(MovingCameraScene):
    def build_table(self,sample_graph):
        top_pos = sample_graph.get_bottom()
        top_pos[1]-=0.5
        bottom_pos = [top_pos[0],-20,0]
        left_pos = [sample_graph.get_left()[0],top_pos[1]-1,0]
        vertical_line = Line(top_pos,bottom_pos)
        horizantal_line = Line(left_pos,[sample_graph.get_right()[0],top_pos[1]-1,0])
        self.play(Write(vertical_line),Write(horizantal_line))
        header = Text("Explored    Frontier",size=0.5)
        header.next_to(horizantal_line,direction=UP)
        self.play(Write(header))
        x1 = horizantal_line.get_bottom()
        x2 = horizantal_line.get_bottom()
        x1[0] = (x1[0] + horizantal_line.get_right()[0]) / 2
        x2[0] = (x2[0] + horizantal_line.get_left()[0]) / 2
        x1[1] -= between_Text_gaps
        x2[1] -= between_Text_gaps
        return x1,x2

    def frontier_table_text_add(self,array,text,pos):
        # new_text = text.copy()
        new_text = Text(text,size=0.5)
        new_text.move_to(pos)
        array.append(new_text)
        pos[1] -= between_Text_gaps
        return new_text

    def explored_table_text_add(self,array,frontier_array,end_pos,start_pos):
        # new_text = text.copy()
        text_obj = frontier_array.pop(0)
        output = text_obj.animate.move_to(end_pos)
        group = VGroup()
        for i in frontier_array:
            group.add(i)
        array.append(text_obj)
        end_pos[1]-= between_Text_gaps
        start_pos[1] += between_Text_gaps
        return output , group.animate.shift(UP*between_Text_gaps)

    def introduction(self):
        header = Tex("Birst First Search Algorithm")
        header.set_width(8)
        from_pos = [header.get_left()[0] - 1, header.get_bottom()[1]-0.5,0]
        to_pos = [header.get_right()[0] + 1, header.get_bottom()[1]-0.5,0]
        line = Line(from_pos,to_pos)
        writer = Tex("Created by Danial Kordmodanlou")
        writer_pos = [(line.get_left()[0] + line.get_right()[0]) / 2 , line.get_bottom()[1] -1,0]
        writer.move_to(writer_pos)
        self.play(Write(header),Write(line))
        self.wait(0.5)
        self.play(Transform(header,Tex("BFS Algorithm")))
        self.play(Write(writer))
        self.wait(1.5)
        return VGroup(header,writer,line)
        
    def start_up_actions(self):
        opening = self.introduction()
        self.play(FadeOut(opening))
        self.wait(0.5)
        explanation = Tex("\\begin{flushleft}Steps : \\end{flushleft}",
        "\\begin{flushleft}1.add root to frontier  \\end{flushleft} ",
        "\\begin{flushleft} 2.pop out from frontier as queue and add it to explored set  \\end{flushleft}", 
        "\\begin{flushleft} 3.find all child nodes and add them to frontier \\newline except repetitive nodes that are in explored or frontier sets \\newline \\end{flushleft}",
        "\\begin{flushleft} 4.check if new nodes are our target :  \\end{flushleft}")
    
        explanation.scale(0.75)
        explanation.to_corner(UL)
        rules = Tex("\\begin{flushleft} 4.1.if TRUE: \\newline \\space return the way from root to target \\newline 4.2.else repeat 2 to 4\\end{flushleft}")
        rules.scale(0.75)
        rules.next_to(explanation[len(explanation)-1].get_right(),buff=0.5)
        brace = Brace(rules,direction=LEFT)
        times = [0.7,3,10,3,2]
        for i in range(len(explanation)):
            self.play(Write(explanation[i],run_time=times[i]))
        self.wait(0.5)
        self.play(Write(brace),Write(rules,run_time=3))
        return VGroup(brace,explanation,rules)

    def show_ending(self):
        self.clear()
        ending_text = Text("Thanks for Watching")
        ending_text.set_color_by_gradient(BLUE,YELLOW)
        self.play(Write(ending_text))
        self.wait(1.5)

    def construct(self):

        opening = self.start_up_actions()
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

        self.play(Transform(opening,sample_graph))
        self.wait(1.5)
        self.remove(opening)
        self.play(sample_graph.animate.scale(0.5))
        self.play(sample_graph.animate.to_edge(UL))
        self.wait(0.5)
        self.play(Write(Line([0,20,0],[0,-20,0]).next_to(sample_graph)))
        

        # Start BFS
        frontier_text_pos , explored_text_pos = self.build_table(sample_graph)

        clone_graph = copy.deepcopy(graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = sample_graph.get_width() + sample_graph.get_center()[0] + 0.5
        RIGHT_X_AREA = 5.5


        frontier = []
        explored = []
        way = []
        frontier_text = []
        explored_text = []


        self.play(Write(self.frontier_table_text_add(frontier_text,clone_graph.root.name,frontier_text_pos))
        ,draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
        draw_root.set_color(BLUE_A)
        self.play(draw_root.animate.scale(1.5))

        frontier.append(clone_graph.root)
        check = True
        while(check):
            if len(frontier) == 0:
                break
            expand_node = frontier.pop(0)
            anim1,anim2 = self.explored_table_text_add(explored_text,frontier_text,explored_text_pos,frontier_text_pos)
            self.play(anim1,anim2)
            explored.append(expand_node)
            if clone_graph.map.__contains__(expand_node):
                for i in clone_graph.map[expand_node]:
                    if i in explored:
                        continue
                    frontier.append(i)
                    draw_root = i.graphics
                    pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                    self.play(Write(self.frontier_table_text_add(frontier_text,i.name,frontier_text_pos))
                        ,draw_root.animate.move_to(pos))
                    draw_root.set_color(BLUE_A)
                    arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=1,buff=draw_root.get_width()*1.5/2,color=YELLOW)
                    i.set_dad(expand_node,arrow)
                    
                    self.play(Write(arrow),draw_root.animate.scale(1.5))
                    self.wait(1)
                    if i.name == "G":
                        temp = i
                        while temp.dad is not None:
                            way.append(temp)
                            temp = temp.dad
                        way.append(temp)
                        way.reverse()
                        for j in way:
                            graphics = j.graphics
                            graphics.set_color(GREEN)
                            if j.arrow is not None:
                                arrow = j.arrow
                                arrow.set_color(GREEN)
                                self.play(Write(arrow))
                                self.add(graphics)
                                self.wait(0.5)
                            else:
                                self.play(Write(graphics))
                        check = False
                        break

                    
        self.show_ending()
    