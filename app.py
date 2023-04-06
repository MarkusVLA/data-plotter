# Work in progress. Now demo will render a 3d sinc function
# using a point cloud. Tested to handle 15e7 points at once on a GTX 1070Ti.

import sys

sys.path.insert(1, "src")
from main import Window

if __name__  == "__main__":
    window = Window(int(1920 / 2), int(1080 / 2), "OpenGL")
    window.main_loop()
