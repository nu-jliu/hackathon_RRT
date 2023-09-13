import sys
import math
import random
import time
import imageio
import numpy as np

from threading import Lock
from matplotlib.pyplot import Axes
from matplotlib.patches import Circle
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Node:
    
    def __init__(self, position):
        self.children: list[Node] = []
        self.parent: Node = None
        self.position: tuple[float, float] = position
        
    def get_distance(self, new_pos: tuple[float, float]):
        x_dist = abs(self.position[0] - new_pos[0])
        y_dist = abs(self.position[1] - new_pos[1])
        
        return math.sqrt(x_dist ** 2 + y_dist ** 2)

class RRT:
    
    def __init__(
        self, 
        root: Node, 
        inc_dist: int, 
        domain: tuple[int, int], 
        num_vert, 
        end_pos: tuple[int, int], 
        do_image: bool
    ):
        self.root = root
        self.inc_dist = inc_dist
        self.domain = domain
        self.num_vert = num_vert
        self.obs: list[tuple[tuple[float, float], float]] = []
        self.end = self.check_point(end_pos)
        self.end_node: Node = None
        self.do_image = do_image
        
        self.generate_obs()
        self.root.position = self.check_point(self.root.position)
        self.positions: list[tuple[float, float]] = [self.root.position]
        # print(self.root.position)
        
        # print(f'size: {self.nu_background.shape}')
        
    def generate_obs(self):
        if self.do_image:
            self.nu_background = imageio.imread("image/N_map.png")
            self.nu_show = np.empty(self.nu_background.shape, dtype='int')
            for row in range(self.nu_background.shape[0]):
                for col in range(self.nu_background.shape[1]):
                    self.nu_show[self.nu_background.shape[0] - 1 - row][col] = self.nu_background[row][col]
                    
                    r, g, b = self.nu_background[row][col]
                    # print(f"r: {r}, g: {g}, b: {b}")
                    if r == 0 and g == 0 and b == 0:
                        self.obs.append(((self.nu_background.shape[1] - 1 - col, row), 1.5))
                        
                
        else:
            self.obs.append(((51, 31), 20))
            self.obs.append(((7.4, 38), 10.4))
            self.obs.append(((4, 85), 4.5))
            self.obs.append(((94, 22), 16))
            self.obs.append(((19, 19.1), 7.7))
            self.obs.append(((26, 2.4), 19))
            self.obs.append(((26, 98), 8.44))
            self.obs.append(((30, 40), 10))
            
        # print(len(self.obs))
        # print(len(self.nu_background))
        # print(len(self.nu_background[0]))
            
    def check_point(self, pos: tuple[float, float]):
        x, y = pos
        domain_x, domain_y = self.domain
        
        while True:
            if self.check_starting_pos((x, y)):
                break
            
            x = random.random() * domain_x
            y = random.random() * domain_y
            
        return x, y
        
    def generate_tree(self, fig: Figure, ax: Axes, do_ploting: bool):
        for i in range(self.num_vert):
            if self.add_vert(fig, ax, do_ploting):
                return
            
        raise ValueError
    
    def check_all_obs(self, old_pos, new_pos):
        for ob in self.obs:
            center_pos, radius = ob
            if not self.check_if_not_intersects(old_pos, new_pos, center_pos, radius):
                return False
            
        return True
    
    def check_if_not_intersects(
        self, 
        pA: tuple[float, float], 
        pB: tuple[float, float], 
        pO: tuple[float, float],
        radius: float
    ):
        dist = self.get_line_point_dist(pA, pB, pO)
        if dist < radius:
            d_AO = self.dist_between_two_points(pA, pO)
            d_BO = self.dist_between_two_points(pB, pO)
            
            if d_AO < radius or d_BO < radius:
                return False
            
            else:
                vec_AO = self.tuple_sub(pO, pA)
                vec_AB = self.tuple_sub(pB, pA)
                
                c_theta1 = np.dot(vec_AB, vec_AO) / (np.linalg.norm(vec_AB) * np.linalg.norm(vec_AO))
                
                vec_BA = self.tuple_sub(pA, pB)
                vec_BO = self.tuple_sub(pO, pB)
                
                c_theta2 = np.dot(vec_BA, vec_BO) / (np.linalg.norm(vec_BA) * np.linalg.norm(vec_BO))
                
                return c_theta1 < 0 or c_theta2 < 0
        else:
            return True
    
    def dist_between_two_points(self, p1: tuple[float, float], p2: tuple[float, float]):
        p1_x, p1_y = p1
        p2_x, p2_y = p2
        
        return math.sqrt((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2)
        
    def check_starting_pos(self, start_pos: tuple[float, float]):
        start_x, start_y = start_pos
        
        for ob in self.obs:
            (center_x, center_y), radius = ob
            
            if (center_x - start_x) ** 2 + (center_y - start_y) ** 2 < radius ** 2:
                return False
            
        return True
    
    def get_line_point_dist(
        self, 
        line_start: tuple[float, float], 
        line_end: tuple[float, float], 
        point: tuple[float, float]
    ):
        p1 = line_start
        p2 = line_end
        p3 = point
        
        return np.linalg.norm(
            np.cross(
                self.tuple_sub(p2, p1), 
                self.tuple_sub(p3, p1)
        )) / np.linalg.norm(
            self.tuple_sub(p2, p1)
        )
        
    def tuple_sub(self, t1, t2):
        return tuple(map(
            lambda i, j:
                i - j,
            t1,
            t2
        ))
            
    def check_all_positions(self, new_pos):
        new_pos_x, new_pos_y = new_pos
        
        for pos in self.positions:
            x, y = pos
            if (new_pos_x - x) ** 2 + (new_pos_y - y) ** 2 < (self.inc_dist ** 2):
                return False
            
        return True
    
    def gen_random_position(self):
        new_pos = self.root.position
        domain_x, domain_y = self.domain
        
        while self.positions.__contains__(new_pos):
            x_rand: float = float(random.random() * domain_x)
            y_rand: float = float(random.random() * domain_y)
            
            new_pos = x_rand, y_rand
            
        return new_pos
        
    def add_vert(self, fig: Figure, ax: Axes, do_plotting: bool):
        while True:
            target_pos = self.gen_random_position()
            
            min_node, min_dist = self.find_min_dist_vert(self.root, target_pos)
            # print(target_pos, min_node.position, min_dist)
            # if min_dist == 0:
                # continue
            
            
            node_x, node_y = min_node.position
            target_x, target_y = target_pos
            dir_move = (
                (target_x - node_x) / min_dist * self.inc_dist, 
                (target_y - node_y) / min_dist * self.inc_dist
            ) 
            new_pos = (node_x + dir_move[0], node_y + dir_move[1])
            
            # print(target_pos, new_pos, min_node.position)
            if self.check_all_obs(min_node.position, new_pos):
                break
            # else:
                # print("Collision")
        
        print(new_pos, min_node.position, min_dist)
        new_node = Node(new_pos)
        
        new_node.parent = min_node
        min_node.children.append(new_node)
        
        self.positions.append(new_node.position)
        
        if do_plotting:
            ax.cla()
            self.plot_all(ax)
            # self.plot_node(self.root, ax)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
        
        if self.check_all_obs(new_pos, self.end):
            end_node = Node(self.end)
            end_node.parent = new_node
            new_node.children.append(end_node)
            self.end_node = end_node
            self.positions.append(self.end)
            return True
        
        else:
            return False
            
                
    def find_min_dist_vert(self, node: Node, target_pos: tuple[float, float]):
        
        if len(node.children) == 0:
            return node, node.get_distance(target_pos)
        
        else:
            min_dist: float = node.get_distance(target_pos)
            min_node: Node = node
            
            for child in node.children:
                min_node_child, min_dist_child = self.find_min_dist_vert(child, target_pos)
                if min_dist_child < min_dist:
                    min_dist = min_dist_child
                    min_node = min_node_child
                    
            return min_node, min_dist
        
    def plot_all(self, ax: Axes):
        ax.set_xlim((0, 100))
        ax.set_ylim((0, 100))
        
        ax.plot([self.end[0]], [self.end[1]], marker='o', color='green', markersize='5')
        ax.plot([self.root.position[0]], [self.root.position[1]], marker='o', color='m', markersize='5')
        
        self.plot_node(self.root, ax)
        
        if self.do_image:
            # nu_show = np.empty(self.nu_background.shape, dtype='int')
            # for row in range(self.nu_background.shape[0]):
            #     for col in range(self.nu_background.shape[1]):
            #         nu_show[self.nu_background.shape[0] - row - 1][col] = self.nu_background[row][col]
            
            ax.imshow(self.nu_show, cmap='gray', origin='upper')
        else:    
            for obst in self.obs:
                (pos_x, pos_y), rad = obst
                
                cir = Circle((pos_x, pos_y), rad, color='black')
                ax.add_patch(cir)
            
        
        if self.end_node != None:
            self.plot_path(self.end_node, ax)
            
    
    def plot_node(self, node: Node, ax: Axes):
        if len(node.children) != 0:
            node_x, node_y = node.position
            
            for child in node.children:
                child_x, child_y = child.position
                
                arr_x = [node_x, child_x]
                arr_y = [node_y, child_y]
                
                ax.plot(arr_x, arr_y, marker='o', color='blue', markersize=1.5)
                
                self.plot_node(child, ax)
                
    def plot_path(self, node: Node, ax: Axes):
        if node != self.root:
            x, y = node.position
            parent_x, parent_y = node.parent.position
            
            x_arr = [x, parent_x]
            y_arr = [y, parent_y]
            
            ax.plot(x_arr, y_arr, color='red', marker='o', markersize=1.5)
            
            self.plot_path(node.parent, ax)
    
    