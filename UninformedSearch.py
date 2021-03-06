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
NODES_SCALE = 1.4



#--------------------------------------------------------- BFS ------------------------------------------------------------------

class BFS_graph_search(MovingCameraScene):


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
        header = Tex("Breadt First Search Algorithm")
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

        opening = self.start_up_actions()

        

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
    
#--------------------------------------------------------- DFS ------------------------------------------------------------------



class DFS_graph_search(MovingCameraScene):


    def explored_table_text_add(self,frontier_index_array,index,array,frontier_array,end_pos,start_pos):
        # new_text = text.copy()
        text_obj = frontier_array.pop(index)
        output = text_obj.animate.move_to(end_pos)
        array.append(text_obj)
        group = VGroup()
        for i in range(len(frontier_index_array)):
            if frontier_index_array[i] > index:
                frontier_index_array[i] -= 1
        for i in range(index,len(frontier_array)):
            group.add(frontier_array[i])
        end_pos[1]-= between_Text_gaps
        start_pos[1] += between_Text_gaps
        return output , group.animate.shift(UP*between_Text_gaps)

    def introduction(self):
        header = Tex("Depth First Search Algorithm")
        header.set_width(8)
        from_pos = [header.get_left()[0] - 1, header.get_bottom()[1]-0.5,0]
        to_pos = [header.get_right()[0] + 1, header.get_bottom()[1]-0.5,0]
        line = Line(from_pos,to_pos)
        writer = Tex("Created by Danial Kordmodanlou")
        writer_pos = [(line.get_left()[0] + line.get_right()[0]) / 2 , line.get_bottom()[1] -1,0]
        writer.move_to(writer_pos)
        self.play(Write(header),Write(line))
        self.wait(0.5)
        self.play(Transform(header,Tex("DFS Algorithm")))
        self.play(Write(writer))
        self.wait(1.5)
        return VGroup(header,writer,line)
        
    def start_up_actions(self):
        sound_path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\sounds\\bensound-creativeminds (mp3cut.net).mp3"
        self.add_sound(sound_path)
        opening = self.introduction()
        self.play(FadeOut(opening))
        self.wait(0.5)
        explanation = Tex("\\begin{flushleft}Steps : \\end{flushleft}",
        "\\begin{flushleft} 1. add root to frontier\\end{flushleft} ",
        "\\begin{flushleft} 2. if frontier is empty there is no answer for this graph\\end{flushleft} ",
        "\\begin{flushleft} 3. pop out deepest node from frontier and add it to the explored set  \\end{flushleft}", 
        "\\begin{flushleft} 4. find all child nodes from selected node and add them to the frontier \\newline if they are not in the explored set and update node state if it is in frontier set \\newline \\end{flushleft}",
        "\\begin{flushleft} 5. check if new nodes include the target node:  \\end{flushleft}",TexTemplate = TexTemplateLibrary)
    
        explanation.scale(0.75)
        explanation.to_corner(UL)
        rules = Tex("\\begin{flushleft} 4.1. if {\\color{red}True}: \\newline \\space return the path \\newline 4.2. else repeat steps 2 to 5\\end{flushleft}")
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
        example_header_tex = Tex("let's see an example of DFS graph search","with goal test on node creation")
        example_header_tex[0].move_to([0,0,0])
        example_header_tex[1].next_to(example_header_tex[0],DOWN)
        self.play(Write(example_header_tex))
        self.wait(1)
        return example_header_tex



    def construct(self):

        opening = self.start_up_actions()
        

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,STATIC_GRAPH_RIGHT_X_AREA,STATIC_GRAPH_LEFT_X_AREA)

        sample_graph_animation(self,opening,sample_graph)

        # Start BFS
        frontier_text_pos , explored_text_pos = build_table(self,sample_graph)



        LEFT_X_AREA = sample_graph.get_width() + sample_graph.get_center()[0] + 0.5
        RIGHT_X_AREA = 5.5


        frontier = []
        explored = []
        way = []
        frontier_text = []
        explored_text = []

        frontier_index_array = []
 



        graph.make_nodes_connected_bi_directional()

        new_graph = GraphSystem.Graph(scale)
        new_graph.has_cost = True
        for i in range(len(graph.branching_factors)):
            new_graph.branching_factors.append(0)
        root = copy.deepcopy(graph.root)
        new_graph.root = root
        
        frontier.append(new_graph.root)

        check = True
        while(check):
            if len(frontier) == 0:
                break
            expand_node = frontier.pop()
            real_expand_node = graph.nodes[expand_node.name]
            explored.append(real_expand_node)
            if graph.map.__contains__(real_expand_node):

                reverse_array = []
                for i in graph.map[real_expand_node]:

                    if i in explored:
                        continue
                    new_node = copy.deepcopy(i)
                    new_node.depth = 0
                    
                    if i.name == "G":
                        check = False
                    reverse_array.append(new_node)
                if len(reverse_array) != 0:
                    for i in range(len(reverse_array)):
                        for j in range(i,len(reverse_array)):
                            if reverse_array[i].name < reverse_array[j].name:
                                reverse_array[i],reverse_array[j] = reverse_array[j],reverse_array[i]
                    for i in reverse_array:
                        frontier.append(i)
                    for i in reverse_array.__reversed__():
                        new_graph.insert(i,expand_node)
                


        new_graph.graph_cleaner()

        
        frontier.clear()
        explored.clear()
        clone_graph = copy.deepcopy(new_graph)


        draw_root = clone_graph.root.graphics
        self.play(Write(frontier_table_text_add(frontier_text,clone_graph.root.name,frontier_text_pos))
        ,draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
        draw_root.set_color(BLUE_A)
        self.play(draw_root.animate.scale(NODES_SCALE))

        frontier.append(clone_graph.root)
        frontier_index_array.append(0)
        check = True
        while(check):
            if len(frontier) == 0:
                break
            expand_node = frontier.pop()
            new_index = frontier_index_array.pop()
            anim1,anim2 = self.explored_table_text_add(frontier_index_array,new_index,explored_text,frontier_text,explored_text_pos,frontier_text_pos)
            self.play(anim1,anim2)
            explored.append(expand_node)
            self.play(expand_node.visual_shape.animate.set_color(YELLOW))
            self.wait(0.7)
            if clone_graph.map.__contains__(expand_node):
                reverse_array = []
                reverse_array_index = []
                temp = len(frontier_index_array)-1
                for i in clone_graph.map[expand_node]:
                    trasformation_node = None
                    if i in explored:
                        continue
                    else:
                        for j in range(len(frontier)):
                            if frontier[j].name == i.name:
                                trasformation_node = frontier[j]
                                new_frontier_index_array = copy.deepcopy(frontier_index_array)
                                for k in range(len(new_frontier_index_array)):
                                    if frontier_index_array[k] == j:
                                        new_index = frontier_index_array.pop(k)
                                        reverse_array_index.append(new_index)
                                        reverse_array.append(i)
                                        frontier.pop(j)
                                        break
                                break



                    if trasformation_node is None:
                        temp+=1
                        reverse_array_index.append(temp)
                        reverse_array.append(i)
                        draw_root = i.graphics
                    else:
                        draw_root = trasformation_node.graphics
                    pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)

                    if trasformation_node is None:
                        self.play(Write(frontier_table_text_add(frontier_text,i.name,frontier_text_pos))
                            ,draw_root.animate.move_to(pos))
                    else:
                        i.graphics.move_to(pos)
                        i.graphics.scale(NODES_SCALE)
                        self.play(draw_root.animate.move_to(pos),FadeOut(trasformation_node.arrow))
                    
                    draw_root.set_color(BLUE_A)
                    arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=expand_node.graphics.get_width()/2,color=YELLOW)
                    i.set_dad(expand_node,arrow)
                    if trasformation_node is None:
                        self.play(Write(arrow),draw_root.animate.scale(NODES_SCALE))
                    else:
                        self.play(Write(arrow))

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
                if len(reverse_array) != 0:
                    for i in reverse_array.__reversed__():
                        frontier.append(i)
                    reverse_array_index.reverse()
                    for i in reverse_array_index:
                        frontier_index_array.append(i)


        self.wait(1)
        show_ending(self)



#--------------------------------------------------------- IDS ------------------------------------------------------------------


#TODO fix(problem as same as DFS)
class IDS_graph_search(MovingCameraScene):


    def explored_table_text_add(self,frontier_index_array,index,array,frontier_array,end_pos,start_pos):
        # new_text = text.copy()
        text_obj = frontier_array.pop(index)
        output = text_obj.animate.move_to(end_pos)
        array.append(text_obj)
        group = VGroup()
        for i in range(len(frontier_index_array)):
            if frontier_index_array[i] > index:
                frontier_index_array[i] -= 1
        for i in range(index,len(frontier_array)):
            group.add(frontier_array[i])
        end_pos[1]-= between_Text_gaps
        start_pos[1] += between_Text_gaps
        return output , group.animate.shift(UP*between_Text_gaps)

    def introduction(self):
        header = Tex("Iterative deepening Search Algorithm")
        header.set_width(8)
        from_pos = [header.get_left()[0] - 1, header.get_bottom()[1]-0.5,0]
        to_pos = [header.get_right()[0] + 1, header.get_bottom()[1]-0.5,0]
        line = Line(from_pos,to_pos)
        writer = Tex("Created by Danial Kordmodanlou")
        writer_pos = [(line.get_left()[0] + line.get_right()[0]) / 2 , line.get_bottom()[1] -1,0]
        writer.move_to(writer_pos)
        self.play(Write(header),Write(line))
        self.wait(0.5)
        self.play(Transform(header,Tex("IDS Algorithm")))
        self.play(Write(writer))
        self.wait(1)
        return VGroup(header,writer,line)
        
    def start_up_actions(self):
        sound_path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\sounds\\bensound-inspire (mp3cut.net).mp3"
        self.add_sound(sound_path)
        opening = self.introduction()
        self.play(FadeOut(opening))
        self.wait(0.5)
        explanation = Tex("\\begin{flushleft}Steps : \\end{flushleft}",
        "\\begin{flushleft} 1. add root to frontier   \\end{flushleft} ",
        "\\begin{flushleft} 2. if frontier is empty then increament depth limit and do steps again\\end{flushleft} ",
        "\\begin{flushleft} 3. pop out deepest node from frontier and add it to the explored set  \\end{flushleft}", 
        "\\begin{flushleft} 4. find all child nodes from selected node and add them to the frontier \\newline except nodes with depth limit or repetitive nodes that are in the explored or frontier sets \\newline \\end{flushleft}",
        "\\begin{flushleft} 5. check if new nodes include the target node:  \\end{flushleft}",TexTemplate = TexTemplateLibrary)
    
        explanation.scale(0.75)
        explanation.to_corner(UL)
        rules = Tex("\\begin{flushleft} 4.1. if {\\color{red}True}: \\newline \\space return the path \\newline 4.2. else repeat steps 2 to 5\\end{flushleft}")
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
        self.wait(2)
        all_group = VGroup(brace,explanation,rules)
        self.play(FadeOut(all_group))
        example_header_tex = Tex("let's see an example of IDS graph search","with goal test on node creation")
        example_header_tex[0].move_to([0,0,0])
        example_header_tex[1].next_to(example_header_tex[0],DOWN)
        self.play(Write(example_header_tex))
        self.wait(1)
        return example_header_tex



    def construct(self):

        opening = self.start_up_actions()

        

        # path = input("enter path : ")
        path = "C:\Danial\Projects\Danial\AI teaching assistance stuff\Artificial-Intelligence-Visualization\input.txt"
        graph = GraphSystem.Graph(scale)
        graph.read_from_file(path)

        # showing sample graph
        sample_graph = graph.show_complete_graph(self,STATIC_GRAPH_RIGHT_X_AREA,STATIC_GRAPH_LEFT_X_AREA)

        sample_graph_animation(self,opening,sample_graph)

        # Start BFS
        frontier_text_pos , explored_text_pos = build_table(self,sample_graph)

        reset_pos = explored_text_pos.copy()

        clone_graph = copy.deepcopy(graph)
        draw_root = clone_graph.root.graphics
        LEFT_X_AREA = sample_graph.get_width() + sample_graph.get_center()[0] + 0.5
        RIGHT_X_AREA = 5.5

        depth_level = 1
        depth_level_Tex = Tex("depth limit: 1")
        depth_level_Tex.move_to([0.25,sample_graph.get_top()[1]-0.25,0])
        self.play(Write(depth_level_Tex))
        frontier = []
        explored = []
        way = []
        frontier_text = []
        explored_text = []

        frontier_index_array = []

        new_elemets = VGroup()

        self.play(Write(frontier_table_text_add(frontier_text,clone_graph.root.name,frontier_text_pos))
        ,draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
        draw_root.set_color(BLUE_A)
        self.play(draw_root.animate.scale(NODES_SCALE))
        new_elemets.add(draw_root)

        frontier.append(clone_graph.root)
        frontier_index_array.append(0)
        check = True
        while(check):
            if len(frontier) == 0:
                depth_level += 1
                for i in explored_text:
                    new_elemets.add(i)
                new_tex = Tex("depth limit: "+ str(depth_level))
                new_tex.move_to([0.25,sample_graph.get_top()[1]-0.25,0])
                self.play(Transform(depth_level_Tex,new_tex),FadeOut(new_elemets))

                # reset values
                explored_text_pos = reset_pos.copy()
                explored_text.clear()
                explored.clear()
                new_elemets = VGroup()
                clone_graph = copy.deepcopy(graph)
                draw_root = clone_graph.root.graphics
                self.play(Write(frontier_table_text_add(frontier_text,clone_graph.root.name,frontier_text_pos))
                ,draw_root.animate.move_to(clone_graph.get_node_relative_pos(clone_graph.root,RIGHT_X_AREA,LEFT_X_AREA)))
                draw_root.set_color(BLUE_A)
                self.play(draw_root.animate.scale(NODES_SCALE))
                new_elemets.add(draw_root)

                frontier.append(clone_graph.root)
                frontier_index_array.append(0)

            expand_node = frontier.pop()
            new_index = frontier_index_array.pop()
            anim1,anim2 = self.explored_table_text_add(frontier_index_array,new_index,explored_text,frontier_text,explored_text_pos,frontier_text_pos)
            self.play(anim1,anim2)
            explored.append(expand_node)
            self.play(expand_node.visual_shape.animate.set_color(YELLOW))
            self.wait(0.6)
            if clone_graph.map.__contains__(expand_node):
                reverse_array = []
                reverse_array_index = []
                temp = len(frontier_index_array)-1
                for i in clone_graph.map[expand_node]:
                    if i in explored or i in frontier or i.depth > depth_level:
                        continue
                    temp+=1
                    reverse_array.append(i)
                    reverse_array_index.append(temp)
                    draw_root = i.graphics
                    pos = clone_graph.get_node_relative_pos(i,RIGHT_X_AREA,LEFT_X_AREA)
                    self.play(Write(frontier_table_text_add(frontier_text,i.name,frontier_text_pos))
                        ,draw_root.animate.move_to(pos))
                    draw_root.set_color(BLUE_A)
                    arrow = Arrow(expand_node.graphics.get_center(),draw_root.get_center(),stroke_width=NODES_SCALE,buff=draw_root.get_width()*NODES_SCALE/2,color=YELLOW)
                    new_elemets.add(arrow)
                    new_elemets.add(draw_root)
                    i.set_dad(expand_node,arrow)
                    
                    self.play(Write(arrow),draw_root.animate.scale(NODES_SCALE))
                    self.wait(0.5)
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
                if len(reverse_array) != 0:
                    for i in reverse_array.__reversed__():
                        frontier.append(i)
                    reverse_array_index.reverse()
                    for i in reverse_array_index:
                        frontier_index_array.append(i)


        self.wait(1)
        show_ending(self)
