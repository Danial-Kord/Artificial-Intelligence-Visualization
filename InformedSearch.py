#!/usr/bin/env python
import copy
from GlobalFunctions import*
from manim import *
# from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
from typing_extensions import runtime
import GraphSystem

scale = 0.5






STATIC_GRAPH_LEFT_X_AREA = -4
STATIC_GRAPH_RIGHT_X_AREA = 4
NODES_SCALE = 1.5




#--------------------------------------------------------- BFS ------------------------------------------------------------------

class A_star_graph_search(MovingCameraScene):


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
        header = Tex("A* Graph Search Algorithm")
        header.set_width(8)
        from_pos = [header.get_left()[0] - 1, header.get_bottom()[1]-0.5,0]
        to_pos = [header.get_right()[0] + 1, header.get_bottom()[1]-0.5,0]
        line = Line(from_pos,to_pos)
        writer = Tex("Created by Danial Kordmodanlou")
        writer_pos = [(line.get_left()[0] + line.get_right()[0]) / 2 , line.get_bottom()[1] -1,0]
        writer.move_to(writer_pos)
        self.play(Write(header),Write(line))
        self.wait(0.5)
        self.play(Write(writer))
        self.wait(1)
        return VGroup(header,writer,line)
        
    def start_up_actions(self):
        sound_path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\sounds\\bensound-creativeminds (mp3cut.net).mp3"
        self.add_sound(sound_path)
        opening = self.introduction()
        self.play(FadeOut(opening))
        self.wait(0.5)
        explanation = Tex("\\begin{flushleft}Steps: \\end{flushleft}",
        "\\begin{flushleft} 1. add root to frontier  \\end{flushleft} ",
        "\\begin{flushleft} 2. if frontier is empty there is no answer for this graph\\end{flushleft} ",
        "\\begin{flushleft} 3. pop out from frontier as queue and add it to the explored set  \\end{flushleft}", 
        "\\begin{flushleft} 4. find all child nodes and add them to the frontier \\newline except repetitive nodes that are in the explored or frontier sets \\newline \\end{flushleft}",
        "\\begin{flushleft} 5. check if new nodes include the target node:  \\end{flushleft}",TexTemplate = TexTemplateLibrary)
    
    
        explanation.scale(0.75)
        explanation.to_corner(UL)
        rules = Tex("\\begin{flushleft} 4.1. if {\\color{red} True}: \\newline \\space return the path \\newline 4.2. else repeat steps 2 to 5\\end{flushleft}")
        rules.scale(0.75)
        rules.next_to(explanation[len(explanation)-1].get_right(),buff=0.7)
        brace = Brace(rules,direction=LEFT,buff=0.1)
        times = [0.7,3,4,4,5.5,2]
        finished_time_delay = [0,1.5,1.5,1.5,3,1.5]
        for i in range(len(explanation)):
            self.play(Write(explanation[i],run_time=times[i]))
            self.wait(finished_time_delay[i])
        self.wait(0.5)
        self.play(Write(brace),Write(rules,run_time=3))
        self.wait(3)
        all_group = VGroup(brace,explanation,rules)
        self.play(FadeOut(all_group))
        example_header_tex = Tex("let's see an example of BFS graph search","with goal test on node creation")
        example_header_tex[0].move_to([0,0,0])
        example_header_tex[1].next_to(example_header_tex[0],DOWN)
        self.play(Write(example_header_tex))
        self.wait(1)
        return example_header_tex



    def construct(self):

        # opening = self.start_up_actions()

        opening = None
        

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,STATIC_GRAPH_RIGHT_X_AREA,STATIC_GRAPH_LEFT_X_AREA)

        sample_graph_animation(self,opening,sample_graph)

        # Start BFS
        frontier_text_pos , explored_text_pos = build_table(self,sample_graph)

        clone_graph = copy.deepcopy(graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = sample_graph.get_width() + sample_graph.get_center()[0] + 0.5
        RIGHT_X_AREA = 5.5


        frontier = []
        explored = []
        way = []
        frontier_text = []
        explored_text = []


        self.play(Write(frontier_table_text_add(frontier_text,clone_graph.root.name,frontier_text_pos))
        ,draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
        draw_root.set_color(BLUE_A)
        self.play(draw_root.animate.scale(NODES_SCALE))

        frontier.append(clone_graph.root)
        check = True
        while(check):
            if len(frontier) == 0:
                break
            expand_node = frontier.pop(0)
            anim1,anim2 = self.explored_table_text_add(explored_text,frontier_text,explored_text_pos,frontier_text_pos)
            self.play(anim1,anim2)
            explored.append(expand_node)
            self.play(expand_node.visual_shape.animate.set_color(YELLOW))
            self.wait(0.7)
            if clone_graph.map.__contains__(expand_node):
                for i in clone_graph.map[expand_node]:
                    if i in explored or i in frontier:
                        continue
                    frontier.append(i)
                    draw_root = i.graphics
                    pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                    self.play(Write(frontier_table_text_add(frontier_text,i.name,frontier_text_pos))
                        ,draw_root.animate.move_to(pos))
                    draw_root.set_color(BLUE_A)
                    arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()*NODES_SCALE/2,color=YELLOW)
                    i.set_dad(expand_node,arrow)
                    
                    self.play(Write(arrow),draw_root.animate.scale(NODES_SCALE))
                    self.wait(1)
                    if i.name == "G":
                        temp = i
                        while temp.dad is not None:
                            way.append(temp)
                            temp = temp.dad
                        way.append(temp)
                        way.reverse()
                        for j in way:
                            circle = j.visual_shape.copy()
                            circle.set_stroke(width= circle.get_stroke_width()*1.8,color = GREEN_C)
                            circle.shift([0,0,1])
                            if j.arrow is not None:
                                arrow = j.arrow
                                self.play(arrow.animate.set_color(GREEN_D))
                            self.play(ShowCreation(circle))
                            self.wait(0.5)
                        check = False
                        break

        self.wait(1)
        show_ending(self)
    