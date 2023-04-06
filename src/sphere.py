from OpenGL.GL import *
from OpenGL.GLU import *

class Sphere:
    
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color

    def draw(self):
        glColor3f(*self.color)
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        glPushMatrix()
        glTranslatef(*self.position)
        gluSphere(quadric, self.radius, 10, 10)
        glPopMatrix()