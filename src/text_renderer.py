import os
import numpy as np
import freetype
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class TextRenderer:
    def __init__(self, font_path, font_size, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        # Load and compile shaders
        with open(os.path.join("shaders", "text_vertex_shader.glsl"), "r") as f:
            vertex_shader = compileShader(f.read(), GL_VERTEX_SHADER)
        with open(os.path.join("shaders", "text_fragment_shader.glsl"), "r") as f:
            fragment_shader = compileShader(f.read(), GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, fragment_shader)

        # Set up vertex buffer object and vertex array object
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        # Initialize FreeType and load the font
        self.face = freetype.Face(font_path)
        self.face.set_pixel_sizes(0, font_size)

        # Set up the texture atlas
        self.glyphs = {}
        self.texture_atlas_width = 1024
        self.texture_atlas_height = 1024
        self.atlas_x = 0
        self.atlas_y = 0
        self.atlas_row_height = 0

        self.texture_atlas = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_atlas)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, self.texture_atlas_width, self.texture_atlas_height, 0, GL_RED, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Load the ASCII characters
        for i in range(32, 128):
            self.load_char(chr(i))

    def load_char(self, char):
        # Load the character glyph
        self.face.load
