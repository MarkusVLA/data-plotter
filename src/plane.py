from OpenGL.GL import *
from OpenGL.GLU import *

class Plane:
    
    def __init__(self, position, size:float, color = (0.1, 0.2, 1.0)) -> None:
        self.size = size
        self.position = position
        self.color = color

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(*self.color)
        glNormal3f(0, 1, 0)
        glVertex3f(-self.size, self.position, -self.size)
        glVertex3f(-self.size, self.position, self.size)
        glVertex3f(self.size, self.position, self.size)
        glVertex3f(self.size, self.position, -self.size)
        glEnd()