between_Text_gaps = 0.35
TABLE_TEXT_SIZE = 0.4
STATIC_GRAPH_MIN_SCALE = 0.5
from manim import *

def build_table(scene,sample_graph):
    top_pos = sample_graph.get_bottom()
    top_pos[1]-=0.5
    bottom_pos = [top_pos[0],-20,0]
    left_pos = [sample_graph.get_left()[0],top_pos[1]-1,0]
    vertical_line = Line(top_pos,bottom_pos)
    horizantal_line = Line(left_pos,[sample_graph.get_right()[0],top_pos[1]-1,0])
    scene.play(Write(vertical_line),Write(horizantal_line))
    explored_header = Text("Explored",size=0.5)
    frontier_header = Text("Frontier",size=0.5)
    x1 = horizantal_line.get_bottom()
    x2 = horizantal_line.get_bottom()
    x1[0] = (x1[0] + horizantal_line.get_right()[0]) / 2
    x2[0] = (x2[0] + horizantal_line.get_left()[0]) / 2
    x1[1] += between_Text_gaps
    x2[1] += between_Text_gaps
    explored_header.move_to(x2)
    frontier_header.move_to(x1)
    scene.play(Write(explored_header),Write(frontier_header))
    x1[1] -= between_Text_gaps*2
    x2[1] -= between_Text_gaps*2
    return x1,x2

def frontier_table_text_add(array,text,pos):
    # new_text = text.copy()
    new_text = Text(text,size=TABLE_TEXT_SIZE)
    new_text.move_to(pos)
    array.append(new_text)
    pos[1] -= between_Text_gaps
    return new_text

def sample_graph_animation(scene,opening,sample_graph):
    scene.play(Transform(opening,sample_graph))
    scene.wait(1.5)
    scene.remove(opening)
    scene.play(sample_graph.animate.scale(STATIC_GRAPH_MIN_SCALE))
    scene.play(sample_graph.animate.to_edge(UL))
    scene.wait(0.5)
    scene.play(Write(Line([0,20,0],[0,-20,0]).next_to(sample_graph)))

def show_ending(self):
    
    self.play(*[FadeOut(mob)for mob in self.mobjects])
    self.wait(0.5)
    ending_text = Text("Thanks for Watching")
    ending_text.set_color_by_gradient(BLUE,YELLOW)
    self.play(Write(ending_text,run_time=1.8))
    self.wait(3)
    self.play(*[FadeOut(mob)for mob in self.mobjects])