import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from scipy.spatial import Delaunay


class Mesh3D:

    def __init__(self, points):
        self.points = np.array(points, dtype=np.float32)
        self.num_points = len(self.points)

        # Perform Delaunay triangulation to form mesh
        tri = Delaunay(self.points[:, [0, 2]])  # Triangulate using only the X and Z coordinates
        self.indices = tri.simplices.flatten()

        # Create VBO and bind data
        self.vbo = vbo.VBO(self.points)
        self.ibo = vbo.VBO(np.array(self.indices, dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)

        # Load shader code
        with open("src/shaders/mesh_vertex_shader.glsl", "r") as f:
            vertex_shader_code = f.read()

        with open("src/shaders/mesh_fragment_shader.glsl", "r") as f:
            fragment_shader_code = f.read()

        # Compile and link shader program
        vertex_shader = shaders.compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
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
