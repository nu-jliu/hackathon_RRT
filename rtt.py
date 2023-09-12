import math

class RRT:
    
    def __init__(self, root, inc_dist):
        self.root: Node = root
        self.inc_dist = inc_dist
        self.num_vert = 0
        
    def add_vert(self, target_pos: tuple[float, float]):
        x, y = target_pos
        
        curr_node = self.root
        
        while len(curr_node.children) != 0:
            
            for node in curr_node.children:
                pass
        
class Node:
    
    def __init__(self, position):
        self.children: list[Node] = []
        self.parent: Node = None
        self.position: tuple[float, float] = position
        
    def get_distance(self, new_pos: tuple[float, float]):
        x_dist = abs(self.position[0] - new_pos[0])
        y_dist = abs(self.position[1] - new_pos[1])
        
        return math.sqrt(x_dist ** 2 + y_dist ** 2)