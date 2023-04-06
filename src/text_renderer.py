import freetype
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader

vertex_shader_code = '''
    #version 330 core
    layout (location = 0) in vec4 vertex;
    out vec2 TexCoords;
    uniform mat4 model;
    uniform mat4 projection;
    void main()
    {
        gl_Position = projection * model * vec4(vertex.xy, 0.0, 1.0);
        TexCoords = vertex.zw;
    }
'''

fragment_shader_code = '''
    #version 330 core
    in vec2 TexCoords;
    out vec4 color;
    uniform sampler2D text;
    uniform vec3 textColor;
    void main()
    {    
        vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
        color = vec4(textColor, 1.0) * sampled;
    }
'''

class TextRenderer:
    def __init__(self, font_file, shader_program=None):
        self.font_file = font_file
        self.shaderProgram = shader_program if shader_program else self.create_shader_program()

        self.Characters, self.VAO, self.VBO = self.initialize_font_resources()

    def create_shader_program(self):
        return compileProgram(
            compileShader(vertex_shader_code, GL_VERTEX_SHADER),
            compileShader(fragment_shader_code, GL_FRAGMENT_SHADER),
        )

    def initialize_font_resources(self):
        face = freetype.Face(self.font_file)
        face.set_char_size(48 * 64)

        Characters = {}
        for ch in range(128):
            face.load_char(chr(ch), freetype.FT_LOAD_RENDER)
            glyph = face.glyph
            glyph_texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, glyph_texture)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RED,
                glyph.bitmap.width,
                glyph.bitmap.rows,
                0,
                GL_RED,
                GL_UNSIGNED_BYTE,
                glyph.bitmap.buffer,
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            Characters[ch] = {
                'texture_id': glyph_texture,
                'size': (glyph.bitmap.width, glyph.bitmap.rows),
                'bearing': (glyph.bitmap_left, glyph.bitmap_top),
                'advance': glyph.advance.x,
            }

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 24 * 6 * 4, None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return Characters, VAO, VBO

    def render_text(self, text, x, y, z, scale, color, model, projection):
        glUseProgram(self.shaderProgram)
        glUniform3f(glGetUniformLocation(self.shaderProgram, "textColor"), *color)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "model"), 1, GL_FALSE, model)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "projection"), 1, GL_FALSE, projection)
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.VAO)

        for c in text:
            ch = self.Characters[ord(c)]
            xpos = x + ch['bearing'][0] * scale
            ypos = y - (ch['size'][1] - ch['bearing'][1]) * scale
            w = ch['size'][0] * scale
            h = ch['size'][1] * scale

            vertices = [
                xpos, ypos + h, z, 0.0, 0.0,
                xpos, ypos, z, 0.0, 1.0,
                xpos + w, ypos, z, 1.0, 1.0,
                xpos, ypos + h, z, 0.0, 0.0,
                xpos + w, ypos, z, 1.0, 1.0,
                xpos + w, ypos + h, z, 1.0, 0.0
            ]

            glBindTexture(GL_TEXTURE_2D, ch['texture_id'])
            glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
            glBufferSubData(GL_ARRAY_BUFFER, 0, len(vertices) * 4, np.array(vertices, dtype='float32'))
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            glDrawArrays(GL_TRIANGLES, 0, 6)

            x += ch['advance'] // 64 * scale

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glUseProgram(0)


