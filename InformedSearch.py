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
DOWN_SCREEN_BOUND = -3.5


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
        # scene.add(vertical_line,horizantal_line)

        Node_header_text = Text("Node",size=TABLE_TEXT_SIZE)
        cost_header_text = Text("Heuristic",size=TABLE_TEXT_SIZE)
        x1 = horizantal_line.get_bottom()
        x2 = horizantal_line.get_bottom()
        x1[0] = (x1[0] + horizantal_line.get_right()[0]) / 2
        x2[0] = (x2[0] + horizantal_line.get_left()[0]) / 2
        x1[1] += between_Text_gaps
        x2[1] += between_Text_gaps
        Node_header_text.move_to(x2)
        cost_header_text.move_to(x1)

        temp_group = VGroup(horizantal_line,cost_header_text,Node_header_text)
        temp_group.shift(UP*0.3)

        group.add(Node_header_text,cost_header_text)
        # scene.add(Node_header_text,cost_header_text)

        for i in nodes:
            x1[1] -= between_Text_gaps*2
            x2[1] -= between_Text_gaps*2
            node = nodes[i]
            node_name = Text(node.name,size=TABLE_TEXT_SIZE)
            huristic = Text(str(node.H),size=TABLE_TEXT_SIZE)
            node.visual_H = huristic
            node.visual_H_name = node_name
            node_name.move_to(x2)
            huristic.move_to(x1)
            # scene.add(node_name,huristic)
            group.add(node_name,huristic)
        table_text = Tex("Heuristic Table")
        table_text.next_to(group,UP)
        # scene.add(table_text)
        group.add(table_text)
        return group

    def sample_graph_animation(scene,opening,sample_graph,table):
        table.shift(DOWN)
        sample_graph.shift(DOWN)
        group = VGroup(table,sample_graph)
        scene.play(Transform(opening,group))
        scene.add(table,sample_graph)
        scene.wait(1.5)
        scene.remove(opening)
        scene.play(sample_graph.animate.scale(STATIC_GRAPH_MIN_SCALE).to_edge(UR),runtime=2)
        scene.play(table.animate.scale(STATIC_TABLE_MIN_SCALE).next_to(sample_graph,DOWN,buff=1.2))
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
        self.wait(0.7)
        return VGroup(header,writer,line)
        
    def start_up_actions(self):
        sound_path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\sounds\\bensound-creativeminds (mp3cut.net).mp3"
        self.add_sound(sound_path)
        opening = self.introduction()
        self.play(FadeOut(opening))
        # self.wait(0.5)
        # explanation = Tex("\\begin{flushleft}Steps: \\end{flushleft}",
        # "\\begin{flushleft} 1. add root to frontier  \\end{flushleft} ",
        # "\\begin{flushleft} 2. if frontier is empty there is no answer for this graph\\end{flushleft} ",
        # "\\begin{flushleft} 3. pop out from frontier as queue and add it to the explored set  \\end{flushleft}", 
        # "\\begin{flushleft} 4. find all child nodes and add them to the frontier \\newline except repetitive nodes that are in the explored or frontier sets \\newline \\end{flushleft}",
        # "\\begin{flushleft} 5. check if new nodes include the target node:  \\end{flushleft}",TexTemplate = TexTemplateLibrary)
    
    
        # explanation.scale(0.75)
        # explanation.to_corner(UL)
        # rules = Tex("\\begin{flushleft} 4.1. if {\\color{red} True}: \\newline \\space return the path \\newline 4.2. else repeat steps 2 to 5\\end{flushleft}")
        # rules.scale(0.75)
        # rules.next_to(explanation[len(explanation)-1].get_right(),buff=0.7)
        # brace = Brace(rules,direction=LEFT,buff=0.1)
        # times = [0.7,3,4,4,5.5,2]
        # finished_time_delay = [0,1.5,1.5,1.5,3,1.5]
        # for i in range(len(explanation)):
        #     self.play(Write(explanation[i],run_time=times[i]))
        #     self.wait(finished_time_delay[i])
        # self.wait(0.5)
        # self.play(Write(brace),Write(rules,run_time=3))
        # self.wait(3)
        # all_group = VGroup(brace,explanation,rules)
        # self.play(FadeOut(all_group))
        example_header_tex = Tex("Let's see an example of A* search")
        example_header_tex.move_to([0,0,0])
        self.play(Write(example_header_tex))
        self.wait(0.7)
        return example_header_tex

    def print_node_cost(self,node,cost,direction=DOWN):
        cost_tex = Tex(cost)
        cost_tex.next_to(node,direction)
        return cost_tex

    def construct(self):

        opening = self.start_up_actions()

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\with edge input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file_with_edge_costs(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,STATIC_GRAPH_RIGHT_X_AREA,STATIC_GRAPH_LEFT_X_AREA)
        


        table = self.make_table(sample_graph,graph.nodes)

        
        self.sample_graph_animation(opening,sample_graph,table)
        self.wait(0.5)
        graph.make_nodes_connected_bi_directional()




        # make A* graph search

        all_nodes = []
        frontier = []

        new_graph = GraphSystem.Graph(scale)
        new_graph.has_cost = True
        for i in range(len(graph.branching_factors)):
            new_graph.branching_factors.append(0)
        root = copy.deepcopy(graph.root)
        new_graph.root = root
        
        new_graph.root.calculated_cost = 0
        frontier.append(new_graph.root)
        all_nodes.append(frontier[0])
        while(True):
            if len(frontier) == 0:
                break
            min = frontier[0].calculated_cost + frontier[0].H
            selected_frontier_index = 0
            for i in range(len(frontier)):
                if frontier[i].calculated_cost + frontier[i].H < min:
                    min = frontier[i].calculated_cost + frontier[i].H
                    selected_frontier_index = i
            expand_node = frontier.pop(selected_frontier_index)
            real_expand_node = graph.nodes[expand_node.name]

            if expand_node.name == "G":
                break
            if graph.map.__contains__(real_expand_node):
                for i in graph.map[real_expand_node]:
                    new_node = copy.deepcopy(i)
                    new_node.depth = 0
                    new_graph.insert(new_node,expand_node)
                    frontier.append(new_node)
                    all_nodes.append(new_node)
                    for x,y in graph.edges:
                        if x.name == expand_node.name and y.name == new_node.name:
                            new_graph.add_edge_cost(expand_node,new_node,graph.edges[x,y])
                            new_node.set_calculated_cost(expand_node.calculated_cost+graph.edges[x,y])  
                            break        


        for i in all_nodes:
            i.calculated_cost = 0
        # Start search
        new_graph.graph_cleaner()
        clone_graph = copy.deepcopy(new_graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = LEFT_SCREEN_BOUND+1 
        RIGHT_X_AREA = sample_graph.get_center()[0] - (sample_graph.get_width()/2+1.5)


        
        frontier = []
        way = []


        self.play(draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)).scale(NODES_SCALE))
        draw_root.set_color(BLUE_A)

        frontier.append(clone_graph.root)
        check = True


        while(check):
            if len(frontier) == 0:
                break
            min = frontier[0].calculated_cost + frontier[0].H
            selected_frontier_index = 0
            for i in range(len(frontier)):
                if frontier[i].calculated_cost + frontier[i].H < min:
                    min = frontier[i].calculated_cost + frontier[i].H
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
                    circle.set_stroke(width= circle.get_stroke_width()*1.8,color = DARK_BLUE)
                    circle.shift([0,0,1])
                    if j.arrow is not None:
                        arrow = j.arrow
                        self.play(arrow.animate.set_color(DARK_BLUE))
                    self.play(ShowCreation(circle))
                    self.wait(0.5)
                check = False
                break
            if clone_graph.map.__contains__(expand_node):
                for i in clone_graph.map[expand_node]:
                    display_cost_tex = clone_graph.add_edge_visual_tex(expand_node,i)
                    target_point = display_cost_tex.get_center()
                    main_graph_display_tex = graph.visual_edges[graph.nodes[expand_node.name],graph.nodes[i.name]]
                    start_point = main_graph_display_tex.get_center()

                    display_cost_tex.move_to(start_point)
                    clone_graph.visual_edges[expand_node,i] = display_cost_tex
                    cost_display_animation = display_cost_tex.animate.move_to(target_point)

                    frontier.append(i)
                    draw_root = i.graphics
                    arrow = None
                    if i.seen is False:
                        pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                        self.play(draw_root.animate.move_to(pos))
                        draw_root.set_color(BLUE_A)
                        
                        # cost placement
                        display_cost_tex = clone_graph.set_edge_visual_tex(expand_node,i,expand_node.graphics.get_center(),pos,str(clone_graph.edges[expand_node,i]))
                        target_point = display_cost_tex.get_center()
                        main_graph_display_tex = graph.visual_edges[graph.nodes[expand_node.name],graph.nodes[i.name]]
                        start_point = main_graph_display_tex.get_center()
                        display_cost_tex.move_to(start_point)
                        clone_graph.visual_edges[expand_node,i] = display_cost_tex
                        cost_display_animation = display_cost_tex.animate.move_to(target_point)

                        arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()*NODES_SCALE/2,color=YELLOW)
                        
                        
                        if expand_node.visual_calculated_cost is not None:
                            self.play(FadeOut(expand_node.visual_calculated_cost),cost_display_animation,Write(arrow),draw_root.animate.scale(NODES_SCALE))
                            expand_node.visual_calculated_cost = None
                        else:
                            self.play(cost_display_animation,Write(arrow),draw_root.animate.scale(NODES_SCALE))
                        
                        

                        i.seen = True


                    else:
                        arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()/2,color=YELLOW)
                        self.play(Write(arrow))
                    self.wait(0.6)   

                    i.set_dad(expand_node,arrow)
                    for x,y in clone_graph.edges:
                        if x.name == expand_node.name and y.name == i.name:
                            i.set_calculated_cost(expand_node.calculated_cost+clone_graph.edges[x,y])
                            calc = ""
                            animates = VGroup()
                            covers_animation = []
                            temp = i
                           
                            animates.add(temp.visual_H)
                            width = float(np.abs(temp.visual_H.get_center() - temp.visual_H_name.get_center())[0] + 0.6)
                            height = float(np.abs(temp.visual_H.get_center() - temp.visual_H_name.get_center())[1] + 0.5)
                            rect = RoundedRectangle(corner_radius=0.7)
                            rect.set_height(height)
                            rect.stretch_to_fit_width(width)
                            rect.set_color(GREEN)
                            rect_data = VGroup(temp.visual_H,temp.visual_H_name)
                            
            
                            
                            # rect.set_height(200)
                            rect.move_to(rect_data.get_center())
                            covers_animation.append(ShowCreation(rect))

                            cover_fade_animations = []
                            cover_fade_animations.append(FadeOut(rect))

                            # width = (clone_graph.visual_edges[temp.dad,temp]).get_width()*4
                            while(temp.dad != None):
                                tex = clone_graph.visual_edges[temp.dad,temp]
                                tex_str = str(clone_graph.edges[temp.dad,temp])
                                if temp.dad.dad is not None:
                                   calc += tex_str + "+"
                                else:
                                   calc += tex_str
                                animates.add(tex.copy())
                                circle = Circle()
                                # circle.set_width(width)
                                circle.scale(scale/3)
                                circle.move_to(tex.get_center())
                                covers_animation.append(ShowCreation(circle))
                                cover_fade_animations.append(FadeOut(circle))
                                temp = temp.dad
                            
                            
                            visual_calculated = Tex("Cost : "+calc + "+" + str(i.H) +" = "+str(i.calculated_cost+i.H))
                            # visual_calculated.to_corner(DL)
                            visual_calculated.move_to([(RIGHT_X_AREA+LEFT_X_AREA)/2,DOWN_SCREEN_BOUND,0])

                            final_result = Tex(str(i.calculated_cost+i.H))
                            i.visual_calculated_cost = final_result
                            # i.visual_calculated_cost.set_width(i.visual_shape.get_width())
                            i.visual_calculated_cost.next_to(i.visual_shape,RIGHT,buff=0.05)
                            # i.visual_calculated_cost.set_width(i.visual_shape.get_width()/2)
                            i.visual_calculated_cost.scale(NODES_SCALE/3)

                            self.play(*covers_animation)
                            self.wait(0.5)
                            self.play(Transform(animates,visual_calculated))
                            self.wait(0.8)
                            self.play(Transform(visual_calculated,i.visual_calculated_cost),FadeOut(animates),*cover_fade_animations)
                            self.remove(visual_calculated)
                            self.add(i.visual_calculated_cost)
                            break
                    



        self.wait(1)
        show_ending(self)
    