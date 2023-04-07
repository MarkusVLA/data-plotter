from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
import numpy as np


class Point:

    """
    Singe CPU rendered point
    """

    def __init__(self, position, color=(1.0, 0.0, 0.0)):
        self.position = position
        self.z_color = self.position[2] / 2.0 + 0.5  # map z coordinate to [0, 1] range
        self.color = (self.position[0] / 20, self.position[1] / 20, self.position[2] / 20)
        

    def draw(self):
        
        glColor3f(*self.color)  # set the point color
        glPointSize(3.0)  # set the point size
        glBegin(GL_POINTS)
        glVertex3f(*self.position)  # render the point
        glEnd()




class PointCloud:

    """
    A GPU rendered point could for visualizing millions of points at once
    """

    def __init__(self, points, color_axis='z'):
        self.points = np.array(points, dtype=np.float32)
        self.vbo = vbo.VBO(self.points)
        self.color_axis = color_axis

        vertex_shader = shaders.compileShader('''
            #version 120
            attribute vec3 position;
            varying vec3 vertex_color;
            uniform mat4 modelview;
            uniform mat4 projection;
            void main() {
                gl_Position = projection * modelview * vec4(position, 1.0);
                vertex_color = vec3((position.x + 3) / 6.0 * 0.4, (position.y + 3) / 6.0, (position.z + 3) / 6.0 * 0.4); // Normalize z coordinate to [0, 1] range for color
            }''', GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader('''
            #version 120
            varying vec3 vertex_color;
            void main() {
                gl_FragColor = vec4(vertex_color, 1.0);
            }''', GL_FRAGMENT_SHADER)

            
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

    def draw(self):
        shaders.glUseProgram(self.shader)

        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection = glGetFloatv(GL_PROJECTION_MATRIX)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, 'modelview'), 1, GL_FALSE, modelview)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, 'projection'), 1, GL_FALSE, projection)

        color_axis = {'x': 0, 'y': 1, 'z': 2}[self.color_axis]
        glUniform1i(glGetUniformLocation(self.shader, 'color_axis'), color_axis)

        try:
            self.vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glDrawArrays(GL_POINTS, 0, len(self.points))
        finally:
            self.vbo.unbind()
            glDisableVertexAttribArray(0)
            shaders.glUseProgram(0)
