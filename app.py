# Work in progress. Now demo will render a 3d sinc function
# using a point cloud. Tested to handle 15e7 points at once on a GTX 1070Ti.
import random
import sys
import numpy as np
sys.path.insert(1, "src")
from window import Window



def read_csv(filepath):
    with open(filepath, "r") as f:
        data = f.readlines()
        for line in data:
            line = line.split(",")
            yield float(line[0]), float(line[1]), float(line[2])


if __name__  == "__main__":

    data = list(read_csv("demo_data.csv"))

    print(data[:1])
    window = Window(int(1920 / 2), int(1080 / 2), "OpenGL", data=data)
    window.main_loop()
