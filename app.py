# Work in progress. Now demo will render a 3d sinc function
# using a point cloud. Tested to handle 15e7 points at once on a GTX 1070Ti.
import random
import sys
import numpy as np
sys.path.insert(1, "src")
from window import Window


def sinc(x, z):
    r = np.sqrt(x**2 + z**2)
    return x, np.sinc(r) * 3, z

def sinc_points():
    points = []
    
    for i in range(400):
        for j in range(400):
            x = 0.03 * (j - 200)
            y = 0.03 * (i - 200)
            points.append(sinc(x,y))

    return points

def generate_random_points(n):
    points = []
    for i in range(n):
        x = random.uniform(-3, 3)
        y = random.uniform(-3, 3)
        z = random.uniform(-3, 3)
        points.append((x, x, z))
    return points





if __name__  == "__main__":
    window = Window(int(1920 / 2), int(1080 / 2), "OpenGL", data=sinc_points())
    window.main_loop()
