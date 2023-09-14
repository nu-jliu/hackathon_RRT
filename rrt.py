import sys
import math
import random
import time
import imageio
import numpy as np
import util

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
        # x_dist = abs(self.position[0] - new_pos[0])
        # y_dist = abs(self.position[1] - new_pos[1])
        
        # return math.sqrt(x_dist ** 2 + y_dist ** 2)
        
        return util.dist_two_points(self.position, new_pos)

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
        self.obstacles: list[tuple[tuple[float, float], float]] = []
        self.end = self.__get_point_no_collision(end_pos)
        self.end_node: Node = None
        self.do_image = do_image
        
        self.__generate_obs()
        self.root.position = self.__get_point_no_collision(self.root.position)
        self.positions: list[tuple[float, float]] = [self.root.position]
        # print(self.root.position)
        
        # print(f'size: {self.nu_background.shape}')
        
    def __generate_obs(self):
        '''
        This method will generate all obstacles on a graph by:
        
        1. If no image input was selected, the obstacle will be hardcoded circles
        
        2. If the image input was selected, it will take the image input and use 
        the image as the source for the obstacle
        '''
        
        if self.do_image:
            self.nu_background = imageio.imread("image/N_map.png")
            self.nu_show = np.empty(self.nu_background.shape, dtype='int')
            for row in range(self.nu_background.shape[0]):
                for col in range(self.nu_background.shape[1]):
                    self.nu_show[self.nu_background.shape[0] - 1 - row][col] = self.nu_background[row][col]
                    
                    r, g, b = self.nu_background[row][col]
                    if r == 0 and g == 0 and b == 0:
                        self.obstacles.append(((self.nu_background.shape[1] - 1 - col, row), 1.5))
                        
                
        else:
            self.obstacles.append(((51, 31), 20))
            self.obstacles.append(((7.4, 38), 10.4))
            self.obstacles.append(((4, 85), 4.5))
            self.obstacles.append(((94, 22), 16))
            self.obstacles.append(((19, 19.1), 7.7))
            self.obstacles.append(((26, 2.4), 19))
            self.obstacles.append(((26, 98), 8.44))
            self.obstacles.append(((30, 40), 10))
            
    def __get_point_no_collision(self, pos_init: tuple[float, float]):
        """It takes the initial position as input and check if collides with one obstable, 
        if it does, it will generate one without collision

        Args:
            pos_init (tuple[float, float]): _description_

        Returns:
            tuple[int, int]: the coordinate of the point without collision
        """
        x, y = pos_init
        domain_x, domain_y = self.domain
        
        while True:
            if self.__check_position_obs_collision((x, y)):
                break
            
            x = random.random() * domain_x
            y = random.random() * domain_y
            
        return x, y
        
    def __check_all_obs(self, from_pos: tuple[float, float], to_pos: tuple[float, float]):
        """It checks if the line collides with one of the obstacles

        Args:
            from_pos (tuple[float, float]): position of the starting point of the line
            to_pos   (tuple[float, float]): position of the end point of the line

        Returns:
            bool: whether the line collides with any one of the obstacles
        """
        
        for ob in self.obstacles:
            center_pos, radius = ob
            if not self.__check_if_not_intersects(from_pos, to_pos, center_pos, radius):
                return False
            
        return True
    
    def __check_if_not_intersects(
        self, 
        pA: tuple[float, float], 
        pB: tuple[float, float], 
        pO: tuple[float, float],
        radius: float
    ):
        """Check if the line intersects with any one of the obstacle circle

        Args:
            pA (tuple[float, float]): starting point of the line
            pB (tuple[float, float]): end point of the line
            pO (tuple[float, float]): center point of the circle
            radius (float): _description_

        Returns:
            bool: True if not collides with any, False if does collide
        """
        
        dist = util.dist_line_point(pA, pB, pO)
        if dist < radius:
            d_AO = util.dist_two_points(pA, pO)
            d_BO = util.dist_two_points(pB, pO)
            
            if d_AO < radius or d_BO < radius:
                return False
            
            else:
                vec_AO = util.tuple_sub(pO, pA)
                vec_AB = util.tuple_sub(pB, pA)
                
                c_theta1 = np.dot(vec_AB, vec_AO) / (np.linalg.norm(vec_AB) * np.linalg.norm(vec_AO))
                
                vec_BA = util.tuple_sub(pA, pB)
                vec_BO = util.tuple_sub(pO, pB)
                
                c_theta2 = np.dot(vec_BA, vec_BO) / (np.linalg.norm(vec_BA) * np.linalg.norm(vec_BO))
                
                return c_theta1 < 0 or c_theta2 < 0
        else:
            return True
    
    def __check_position_obs_collision(self, pos: tuple[float, float]):
        """check if the position is in one of the obstacle

        Args:
            pos (tuple[float, float]): the position coordinate

        Returns:
            bool: true if not collide with any one of them
        """
        
        x, y = pos
        
        for ob in self.obstacles:
            (center_x, center_y), radius = ob
            
            if (center_x - x) ** 2 + (center_y - y) ** 2 < radius ** 2:
                return False
            
        return True
    
    def __check_all_positions(self, new_pos: tuple[float, float]):
        """check if a new line would collides with one existing

        Args:
            new_pos (tuple[float, float]): the coordinates of the new position

        Returns:
            bool: _description_
        """
        
        new_pos_x, new_pos_y = new_pos
        
        for pos in self.positions:
            x, y = pos
            if (new_pos_x - x) ** 2 + (new_pos_y - y) ** 2 < (self.inc_dist ** 2):
                return False
            
        return True
    
    def generate_tree(self, fig: Figure, ax: Axes, do_ploting: bool):
        """Generate the RRT tree for solving the problem, the method to call in main function

        Args:
            fig (Figure): figure to plot on
            ax (Axes): axes for plotting
            do_ploting (bool): if the program will plot the tree as solving

        Raises:
            ValueError: if not any solution has been found
        """
        
        for i in range(self.num_vert):
            if self.__add_vert(fig, ax, do_ploting):
                return
            
        raise ValueError
    
    # def get_dist_between_two_points(self, p1: tuple[float, float], p2: tuple[float, float]):
    #     p1_x, p1_y = p1
    #     p2_x, p2_y = p2
        
    #     return math.sqrt((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2)
        
    
    
    # def get_line_point_dist(
    #     self, 
    #     line_start: tuple[float, float], 
    #     line_end: tuple[float, float], 
    #     point: tuple[float, float]
    # ):
    #     p1 = line_start
    #     p2 = line_end
    #     p3 = point
        
    #     return np.linalg.norm(
    #         np.cross(
    #             util.tuple_sub(p2, p1), 
    #             util.tuple_sub(p3, p1)
    #     )) / np.linalg.norm(
    #         util.tuple_sub(p2, p1)
    #     )
        
    # def tuple_sub(self, t1, t2):
    #     return tuple(map(
    #         lambda i, j:
    #             i - j,
    #         t1,
    #         t2
    #     ))
            
    
    
    def __gen_random_position(self):
        """Generate a random position

        Returns:
            tuple[float, float]: coordinates of the random positino in the map generated
        """
        
        new_pos = self.root.position
        domain_x, domain_y = self.domain
        
        while self.positions.__contains__(new_pos):
            x_rand: float = float(random.random() * domain_x)
            y_rand: float = float(random.random() * domain_y)
            
            new_pos = x_rand, y_rand
            
        return new_pos
        
    def __add_vert(self, fig: Figure, ax: Axes, do_plotting: bool):
        """Randomly generate one vertice edge length of delta without any collision

        Args:
            fig (Figure): figure to plot on
            ax (Axes): axes for plotting
            do_plotting (bool): if do the plotting

        Returns:
            bool: True if the solution has been found
        """
        
        while True:
            target_pos = self.__gen_random_position()
            
            min_node, min_dist = self.__find_nearest_neighbor_node_dist(self.root, target_pos)
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
            if self.__check_all_obs(min_node.position, new_pos) and self.__check_all_positions(new_pos):
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
            # self.__plot_node(self.root, ax)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
        
        if self.__check_all_obs(new_pos, self.end):
            end_node = Node(self.end)
            end_node.parent = new_node
            new_node.children.append(end_node)
            self.end_node = end_node
            self.positions.append(self.end)
            return True
        
        else:
            return False
            
                
    def __find_nearest_neighbor_node_dist(self, node: Node, target_pos: tuple[float, float]):
        """find the node and the distance that is nearest to the random generated point

        Args:
            node (Node): the parent to to start with
            target_pos (tuple[float, float]): the target location, random generated one

        Returns:
            tuple[Node, float]: the node closest to the point and the distance between
                                the node and the point 
        """
        
        if len(node.children) == 0:
            return node, node.get_distance(target_pos)
        
        else:
            min_dist: float = node.get_distance(target_pos)
            min_node: Node = node
            
            for child in node.children:
                min_node_child, min_dist_child = self.__find_nearest_neighbor_node_dist(child, target_pos)
                if min_dist_child < min_dist:
                    min_dist = min_dist_child
                    min_node = min_node_child
                    
            return min_node, min_dist
        
    def plot_all(self, ax: Axes):
        """plotting method, used for plot the result, or progress

        Args:
            ax (Axes): axes to plot on
        """
        
        ax.set_xlim((0, 100))
        ax.set_ylim((0, 100))
        
        ax.plot([self.end[0]], [self.end[1]], marker='o', color='green', markersize=7)
        ax.plot([self.root.position[0]], [self.root.position[1]], marker='o', color='m', markersize=7)
        
        self.__plot_node(self.root, ax)
        
        if self.do_image:
            ax.imshow(self.nu_show, cmap='gray', origin='upper')
        
        else:    
            for obst in self.obstacles:
                (pos_x, pos_y), rad = obst
                
                cir = Circle((pos_x, pos_y), rad, color='black')
                ax.add_patch(cir)
            
        
        if self.end_node != None:
            self.__plot_path(self.end_node, ax)
            
    
    def __plot_node(self, node: Node, ax: Axes):
        """plot the node and line connected to all of its child

        Args:
            node (Node): node to plot
            ax (Axes): axes to plot on
        """
        
        if len(node.children) != 0:
            node_x, node_y = node.position
            
            for child in node.children:
                child_x, child_y = child.position
                
                arr_x = [node_x, child_x]
                arr_y = [node_y, child_y]
                
                ax.plot(arr_x, arr_y, marker='o', color='blue', markersize=1.8)
                
                self.__plot_node(child, ax)
                
    def __plot_path(self, node: Node, ax: Axes):
        """plot the finalpath from the start to goal

        Args:
            node (Node): node to plot
            ax (Axes): axes to plot on
        """
        
        if node != self.root:
            x, y = node.position
            parent_x, parent_y = node.parent.position
            
            x_arr = [x, parent_x]
            y_arr = [y, parent_y]
            
            ax.plot(x_arr, y_arr, color='red', marker='o', markersize=1.8)
            
            self.__plot_path(node.parent, ax)
    
    