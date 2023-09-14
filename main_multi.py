import sys
import imageio
import threading
import time

import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib.figure import Figure

from rrt import RRT
from rrt import Node

LOCK = threading.Lock()

tree: RRT = None

def try_solve(ax: Axes, fig: Figure):
    global tree
    tree.generate_tree(ax, fig, do_ploting=False)
    print(len(tree.positions))
    
def plot_tree(fig: Figure, ax: Axes):
    
    while True:
        global tree
        if tree != None:
            ax.cla()
            
            tree.plot_all(ax)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage main.py <number of iteration>")
        sys.exit(1)
        
    
    root: Node = Node((40.0, 40.0))
    inc = 1
    domain = (100, 100)
    K_val = int(sys.argv[1])
    # sys.setrecursionlimit(K_val ** 2)

    tree = RRT(root, inc, domain, K_val, (60, 60), True)
    
    print(tree.obstacles)
    print(tree.root.position)

    plt.ion()
    fig, ax = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    
    # thread_plot = threading.Thread(target=plot_tree, args=(fig, ax))
    thread_solve = threading.Thread(target=try_solve, args=(ax, fig))
    # thread_plot.daemon = True
    
    thread_solve.start()
    
    plot_tree(fig, ax)
    thread_solve.join()