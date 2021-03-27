#!/usr/bin/env python
import copy
from random import sample

from numpy.core.fromnumeric import size
from GlobalFunctions import*
from manim import *
# from manimlib import *
from manimlib.constants import FRAME_HEIGHT, FRAME_Y_RADIUS
import numpy as np
from typing_extensions import runtime
import GraphSystem

scale = 0.5




LEFT_SCREEN_BOUND = -7.5


STATIC_GRAPH_LEFT_X_AREA = -2
STATIC_GRAPH_RIGHT_X_AREA = 6
NODES_SCALE = 1.5
between_Text_gaps = 0.3
TABLE_TEXT_SIZE = 0.6

STATIC_GRAPH_MIN_SCALE = 0.5
STATIC_TABLE_MIN_SCALE = 0.7


#--------------------------------------------------------- BFS ------------------------------------------------------------------

class A_star_graph_search(MovingCameraScene):

    def make_table(scene,sample_graph,nodes):

        group = VGroup()
        top_pos = sample_graph.get_left()
       
        top_pos[1] = sample_graph.get_top()[1]-1

        right_pos = [sample_graph.get_left()[0]-0.2,top_pos[1]-1,0]
        left_pos = [LEFT_SCREEN_BOUND,top_pos[1]-1,0]

        top_pos[0] = ((right_pos[0] + left_pos[0])/2)

        bottom_pos = [top_pos[0],top_pos[1] - (len(nodes.keys()) *(TABLE_TEXT_SIZE) + (top_pos[1] - right_pos[1])),0]

        vertical_line = Line(top_pos,bottom_pos)
        horizantal_line = Line(left_pos,right_pos)

        group.add(vertical_line,horizantal_line)
        scene.add(vertical_line,horizantal_line)

        Node_header_text = Text("Node",size=TABLE_TEXT_SIZE)
        cost_header_text = Text("Hiuristic",size=TABLE_TEXT_SIZE)
        x1 = horizantal_line.get_bottom()
        x2 = horizantal_line.get_bottom()
        x1[0] = (x1[0] + horizantal_line.get_right()[0]) / 2
        x2[0] = (x2[0] + horizantal_line.get_left()[0]) / 2
        x1[1] += between_Text_gaps
        x2[1] += between_Text_gaps
        Node_header_text.move_to(x2)
        cost_header_text.move_to(x1)
        group.add(Node_header_text,cost_header_text)
        scene.add(Node_header_text,cost_header_text)

        for i in nodes:
            x1[1] -= between_Text_gaps*2
            x2[1] -= between_Text_gaps*2
            node = nodes[i]
            node_name = Text(node.name,size=TABLE_TEXT_SIZE)
            huristic = Text(str(node.H),size=TABLE_TEXT_SIZE)
            node_name.move_to(x2)
            huristic.move_to(x1)
            scene.add(node_name,huristic)
            group.add(node_name,huristic)
        table_text = Tex("Huristic Table")
        table_text.next_to(group,UP)
        scene.add(table_text)
        group.add(table_text)
        return group

    def sample_graph_animation(scene,opening,sample_graph,table):
        scene.play(Transform(opening,sample_graph))
        scene.wait(1.5)
        scene.remove(opening)
        scene.play(sample_graph.animate.scale(STATIC_GRAPH_MIN_SCALE).to_edge(UR),runtime=2)
        scene.play(table.animate.scale(STATIC_TABLE_MIN_SCALE).next_to(sample_graph,DOWN))
        scene.wait(0.5)
        scene.play(Write(Line([0,20,0],[0,-20,0]).next_to(sample_graph,LEFT)))


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

    def print_node_cost(self,node,cost,direction=DOWN):
        cost_tex = Tex(cost)
        cost_tex.next_to(node,direction)
        return cost_tex

    def construct(self):

        # opening = self.start_up_actions()

        

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\with edge input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file_with_edge_costs(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,STATIC_GRAPH_RIGHT_X_AREA,STATIC_GRAPH_LEFT_X_AREA)
        

        self.add(sample_graph)
        table = self.make_table(sample_graph,graph.nodes)
        self.wait(3)

        tt = Circle()
        self.sample_graph_animation(tt,sample_graph,table)
        graph.make_nodes_connected_bi_directional()




        # make A* graph search

        # A_Start_Graph = GraphSystem.Graph(scale)
        # A_Start_Graph


        # Start search

        clone_graph = copy.deepcopy(graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = LEFT_SCREEN_BOUND+1 
        RIGHT_X_AREA = sample_graph.get_center()[0] - (sample_graph.get_width() +  + 0.5)


        frontier = []
        way = []


        self.play(draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)).scale(NODES_SCALE))
        draw_root.set_color(BLUE_A)

        frontier.append(clone_graph.root)
        check = True


        while(check):
            if len(frontier) == 0:
                break
            min = frontier[0].calculated_cost
            selected_frontier_index = 0
            for i in range(len(frontier)):
                if frontier[i].calculated_cost < min:
                    min = frontier[i].calculated_cost
                    selected_frontier_index = i
            expand_node = frontier.pop(selected_frontier_index)
            
            self.play(expand_node.visual_shape.animate.set_color(YELLOW))
            self.wait(0.7)
            if expand_node.name == "G":
                temp = expand_node
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
            if clone_graph.map.__contains__(expand_node):
                for i in clone_graph.map[expand_node]:
                    for x,y in clone_graph.edges:
                        if x.name == expand_node.name and y.name == i.name:
                           i.set_calculated_cost(i.calculated_cost+clone_graph.edges[x,y])
                           break
                    frontier.append(i)
                    draw_root = i.graphics
                    arrow = None
                    if i.seen is False:
                        pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                        self.play(draw_root.animate.move_to(pos))
                        draw_root.set_color(BLUE_A)
                        arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()*NODES_SCALE/2,color=YELLOW)
                        i.seen = True
                        self.play(Write(arrow),draw_root.animate.scale(NODES_SCALE))
                    else:
                        arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()/2,color=YELLOW)
                        self.play(Write(arrow))
                    self.wait(0.6)                    
                    i.set_dad(expand_node,arrow)
                    



        self.wait(1)
        show_ending(self)
    