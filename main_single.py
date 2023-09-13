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

def try_solve():
    
    # LOCK.acquire()
    global tree
    tree.generate_tree()
    # LOCK.release()
    
def plot_tree(fig: Figure, ax: Axes):
    
    while True:
        # LOCK.acquire()
        global tree
        if tree != None:
            ax.cla()
            
            tree.plot_all(ax)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            # time.sleep(0.1)
        # LOCK.release()
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage main.py <number of iteration>")
        sys.exit(1)
        
    
    root: Node = Node((40, 40))
    inc = 1
    domain = (100, 100)
    K_val = int(sys.argv[1])
    # sys.setrecursionlimit(K_val ** 2)

    tree = RRT(root, inc, domain, K_val, (60, 60))
    
    print(len(tree.obs))
    print(tree.root.position)
    
    # print(imageio.imread("./image/N_map.png"))
    # tree.add_vert()
    # tree.add_vert()
    plt.ion()
    fig, ax = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    
    # thread_plot = threading.Thread(target=plot_tree, args=(fig, ax))
    # thread_solve = threading.Thread(target=try_solve, args=())
    # thread_plot.daemon = True
    
    # thread_solve.start()
    
    # plot_tree(fig, ax)
    # thread_solve.join()
    # thread_plot.start()
    # thread_plot.join()
    # plt.show()
    try:
        # tree.generate_tree(ax=ax, fig=fig, do_ploting=True)
        pass
    except ValueError:
        print("No solution found")
        sys.exit(1)
    else:
        plt.ioff()
        print(len(tree.positions))
        # print(root.get_distance((20, 30)))
        # print(list(map(lambda node: node.position, tree.root.children)), tree.positions)
        # fig, ax = plt.subplots()
        fig.set_figheight(15)
        fig.set_figwidth(15)
        ax.set_title("Rapidly-Exporing Random Tree")
        # ax.plot([0,1], [2, 3])
        # ax.plot([1, 2], [4, 7])
        ax.cla()
        tree.plot_all(ax)
        # ax.axis('equal')
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.show()
        
        
    
    
    