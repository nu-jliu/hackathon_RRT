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
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage main.py <number of iteration>")
        sys.exit(1)
        
    
    root: Node = Node((40, 40))
    inc = 1
    domain = (100, 100)
    K_val = int(sys.argv[1])
    # sys.setrecursionlimit(K_val ** 2)

    tree = RRT(root, inc, domain, K_val, end_pos=(60, 60), do_image=True)
    
    print(len(tree.obstacles))
    print(tree.root.position)
    plt.ion()
    fig, ax = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    ax.set_xlim(xmin=0, xmax=100)
    ax.set_ylim(ymin=0, ymax=100)
    
    try:
        tree.generate_tree(ax=ax, fig=fig, do_ploting=True)
        pass
    except ValueError:
        print("No solution found")
        sys.exit(1)
    else:
        plt.ioff()
        print(len(tree.positions))
        ax.set_title("Rapidly-Exporing Random Tree")
        ax.cla()
        tree.plot_all(ax)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.show()
        
        
    
    
    