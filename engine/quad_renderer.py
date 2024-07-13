import OpenGL.GL as gl
import numpy as np
import ctypes

class QuadRenderer:
    def __init__(self):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.setup_quad()

    def setup_quad(self):
        quad_vertices = np.array([
            -1.0,  1.0,  0.0,  1.0,
            -1.0, -1.0,  0.0,  0.0,
             1.0, -1.0,  1.0,  0.0,

            -1.0,  1.0,  0.0,  1.0,
             1.0, -1.0,  1.0,  0.0,
             1.0,  1.0,  1.0,  1.0,
        ], dtype=np.float32)

        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))

        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

    def render(self):
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        gl.glBindVertexArray(0)

    def cleanup(self):
        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo])
