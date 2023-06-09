import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random

from camera import Camera
from point import PointCloud
from coordinate_axes import CoordinateAxes
from cube import Cube 
from plane import Plane
from mesh import Mesh3D


class Window:

    def __init__(self, width, height, title, data:list):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")
        self.width = width
        self.damping_factor = 0.1
        self.scroll_damping_factor = 0.1
        self.height = height
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create window")

        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.resize_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_position_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        self.camera = Camera(radius=10, angle_x=0, angle_y=0)

        self.mouse_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.axes = CoordinateAxes(length=7.0, x_offset=-3.0, y_offset=-3.0, z_offset=-3.0)

        #self.data = generate_random_points(150000)
        self.data = data
        #self.data = load_points_from_csv("data/cobblestone_10k.csv")
        self.p_cloud = PointCloud(self.data, color_axis='y')
        #self.cube = Cube((0,0,0), 1, (1.0, 0, 0))
        #self.plane = Plane(position=(-1.0,-1.0,-1.0),grid_scale=0.2, rotation=(0,90,90), color=(0.5,0.5,0.5,0.5))
        self.mesh = Mesh3D(data)
        self.setup_camera() # Configure camera


    def setup_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, self.width / self.height, 0.5, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def resize_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def key_callback(self, window, key, scancode, action, mods):
        pass

    def scroll_callback(self, window, xoffset, yoffset):
        # Multiply the scroll offset by the damping factor
        self.camera.adjust_radius(-yoffset * self.scroll_damping_factor)

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.mouse_dragging = True
                self.last_mouse_x, self.last_mouse_y = glfw.get_cursor_pos(window)
            elif action == glfw.RELEASE:
                self.mouse_dragging = False

    #if self.mouse_dragging:
    def cursor_position_callback(self, window, xpos, ypos):
        if self.mouse_dragging:
            dx = xpos - self.last_mouse_x
            dy = ypos - self.last_mouse_y

            self.camera.angle_x -= dy * self.damping_factor
            self.camera.angle_y += dx * self.damping_factor

        # Update the last mouse position continuously
        self.last_mouse_x = xpos
        self.last_mouse_y = ypos

    def handle_input(self):
        glfw.poll_events()

    def update(self):
        pass
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        camera_pos = self.camera.get_camera_position()
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 1, 0)

        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

        # Draw the point cloud
        #self.p_cloud.draw()
        self.axes.draw()
        self.mesh.draw()

        glDisable(GL_COLOR_MATERIAL)

        glfw.swap_buffers(self.window)


    def main_loop(self):
        while not glfw.window_should_close(self.window):
            self.handle_input()
            self.update()
            self.render()

        glfw.terminate()

# if __name__ == "__main__":
    # window = Window(int(1920 / 2), int(1080 / 2), "OpenGL")
    # window.main_loop()


