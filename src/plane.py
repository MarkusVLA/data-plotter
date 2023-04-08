from OpenGL.GL import *
from OpenGL.GLU import *


class Plane:
    def __init__(self, position=(0.0, 0.0, 0.0), size=3, color=(0.4, 0.4, 0.4, 0.5), line_color=(0.8, 0.8, 0.8),
                 grid_scale=2.0, rotation=(0.0, 0.0, 0.0)) -> None:
        self.size = size
        self.position = position
        self.color = color
        self.line_color = line_color
        self.grid_scale = grid_scale
        self.grid_is_on = True
        self.plane_is_on = False
        self.rotation = rotation

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        if self.plane_is_on:
            glBegin(GL_QUADS)
            glColor4f(*self.color)
            glNormal3f(0, 1, 0)
            glVertex3f(-self.size, 0, -self.size)
            glVertex3f(-self.size, 0, self.size)
            glVertex3f(self.size, 0, self.size)
            glVertex3f(self.size, 0, -self.size)
            glEnd()

        if self.grid_is_on:
            self.draw_grid()

        glPopMatrix()

    def draw_grid(self):
        glColor3f(*self.line_color)
        #glLineWidth(1.0)  # Set the line width
        for i in range(int(-self.size / self.grid_scale), int(self.size / self.grid_scale) + 1):
            glBegin(GL_LINES)
            glVertex3f(i * self.grid_scale, 0, -self.size)
            glVertex3f(i * self.grid_scale, 0, self.size)
            glVertex3f(-self.size, 0, i * self.grid_scale)
            glVertex3f(self.size, 0, i * self.grid_scale)
            glEnd()
        #glLineWidth(1.0)  # Reset the line width to the default value
