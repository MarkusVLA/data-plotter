from OpenGL.GL import *
from OpenGL.GLU import *
from plane import Plane
from text_renderer import TextRenderer

class CoordinateAxes:

    def __init__(self, length=1.0, x_offset=0.0, y_offset=0.0, z_offset=0.0):
        self.length = length
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset

        self.x_plane = Plane(position=(0, self.length * 0.5, self.length * 0.5), size=self.length / 2, color=(0.9, 0.7, 0.7, 0.3), rotation=(0, 0, 90), grid_scale=0.5)
        self.y_plane = Plane(position=(self.length * 0.5, self.length * 0.5, 0), size=self.length / 2, color=(0.7, 0.9, 0.7, 0.3), rotation=(90, 0, 0), grid_scale=0.5)
        self.z_plane = Plane(position=(self.length * 0.5, 0, self.length * 0.5), size=self.length / 2, color=(0.7, 0.7, 0.9, 0.3), grid_scale=0.5)

        #self.text_renderer = TextRenderer(font_size=16, font_path="fonts/Arial.ttf", window_width=1920, window_height=1080)

    
    
    def draw_arrow_tip(self, base_radius, height, slices, stacks):
        quadric = gluNewQuadric()
        gluCylinder(quadric, base_radius, 0.0, height, slices, stacks)
        gluDisk(quadric, 0.0, base_radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, self.z_offset)
        glLineWidth(3.0)  # Set the line width
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
        glLineWidth(1.0)  # Reset the line width to the default value

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
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.x_plane.draw()
        self.y_plane.draw()
        self.z_plane.draw()

        glDisable(GL_BLEND)
        glPopMatrix()


        #  # Enable 2D text rendering
        # glDisable(GL_BLEND)
        # glPopMatrix()

        # # Save matrices
        # glMatrixMode(GL_PROJECTION)
        # glPushMatrix()
        # glLoadIdentity()
        # gluOrtho2D(0, 800, 0, 600)  # Set the screen dimensions (modify as needed)

        # glMatrixMode(GL_MODELVIEW)
        # glPushMatrix()
        # glLoadIdentity()

        # # Draw labels
        # self.text_renderer.draw_text('x', 400 + self.length * 50, 300, 0)  # Modify position as needed
        # self.text_renderer.draw_text('y', 400, 300 + self.length * 50, 0)  # Modify position as needed
        # self.text_renderer.draw_text('z', 400, 300, 0)  # Modify position as needed

        # # Restore matrices
        # glMatrixMode(GL_MODELVIEW)
        # glPopMatrix()

        # glMatrixMode(GL_PROJECTION)
        # glPopMatrix()

        # glMatrixMode(GL_MODELVIEW)

