from rrt import RRT
from rrt import Node
import sys

import matplotlib.pyplot as plt
import imageio

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage main.py <number of iteration>")
        sys.exit(1)
        
    
    
    root: Node = Node((50.0, 50.0))
    inc = 1
    domain = (100, 100)
    K_val = int(sys.argv[1])
    # sys.setrecursionlimit(K_val ** 2)
    
    tree = RRT(root, inc, domain, K_val)
    
    
    print(tree.obs)
    print(tree.root.position)
    # print(imageio.imread("./image/N_map.png"))
    # tree.add_vert()
    # tree.add_vert()
    try:
        tree.generate_tree()
    except ValueError:
        print("No solution found")
        sys.exit(1)
    else:
        print(len(tree.positions))
        # print(root.get_distance((20, 30)))
        # print(list(map(lambda node: node.position, tree.root.children)), tree.positions)
        
        fig, ax = plt.subplots()
        ax.set_title("Rapidly-Exporing Random Tree")
        # ax.plot([0,1], [2, 3])
        # ax.plot([1, 2], [4, 7])
        tree.plot_all(ax)
        # ax.axis('equal')
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        
        plt.show()
    
    
    