from OpenGL.GL import *
from OpenGL.GLU import *

class CoordinateAxes:

    def __init__(self, length=1.0, x_offset=0.0, y_offset=0.0, z_offset=0.0):
        self.length = length
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        

    def draw_arrow_tip(self, base_radius, height, slices, stacks):
        quadric = gluNewQuadric()
        gluCylinder(quadric, base_radius, 0.0, height, slices, stacks)
        gluDisk(quadric, 0.0, base_radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, self.z_offset)

        glBegin(GL_LINES)

        # X-axis (red)
        glColor3f(0.9, 0.7, 0.7)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.length, 0.0, 0.0)

        # Y-axis (green)
        glColor3f(0.7, 0.9, 0.7)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.length, 0.0)

        # Z-axis (blue)
        glColor3f(0.7, 0.7, 0.9)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.length)

        glEnd()

        # Draw arrow tips
        arrow_tip_radius = 0.01 * self.length
        arrow_tip_height = 0.04 * self.length
        slices = 16
        stacks = 1

        # X-axis tip (red)
        glColor3f(0.9, 0.7, 0.7)
        glPushMatrix()
        glTranslatef(self.length, 0.0, 0.0)
        glRotatef(90, 0, 1, 0)
        self.draw_arrow_tip(arrow_tip_radius, arrow_tip_height, slices, stacks)
        glPopMatrix()

        # Y-axis tip (green)
        glColor3f(0.7, 0.9, 0.7)
        glPushMatrix()
        glTranslatef(0.0, self.length, 0.0)
        glRotatef(-90, 1, 0, 0)
        self.draw_arrow_tip(arrow_tip_radius, arrow_tip_height, slices, stacks)
        glPopMatrix()

        # Z-axis tip (blue)
        glColor3f(0.7, 0.7, 0.9)
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.length)
        glRotatef(0, 1, 0, 0)
        self.draw_arrow_tip(arrow_tip_radius, arrow_tip_height, slices, stacks)
        glPopMatrix()

        glPopMatrix()


