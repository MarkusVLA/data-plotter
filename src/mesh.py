import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class Mesh3D:

    def __init__(self, points):
        self.points = np.array(points, dtype=np.float32)
        self.num_points = len(self.points)

        # Generate indices for triangles
        self.indices = []
        for i in range(0, self.num_points, 3):
            self.indices.extend([i, i+1, i+2])

        # Create VBO and bind data
        self.vbo = vbo.VBO(self.points)
        self.ibo = vbo.VBO(np.array(self.indices, dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)

        # Create shader program
        vertex_shader = shaders.compileShader('''
            #version 120

            attribute vec3 position;
            varying vec3 vertex_color;

            uniform mat4 modelview;
            uniform mat4 projection;

            void main() {
                gl_Position = projection * modelview * vec4(position, 1.0);
                vertex_color = vec3((position.x + 1.0) / 2.0, (position.y + 1.0) / 2.0, (position.z + 1.0) / 2.0);
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

        try:
            self.vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

            self.ibo.bind()
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        finally:
            self.vbo.unbind()
            glDisableVertexAttribArray(0)
            self.ibo.unbind()

            shaders.glUseProgram(0)
