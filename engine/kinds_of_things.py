from typing import Optional
import OpenGL.GL as gl
import numpy as np
import ctypes
from engine.thing import Thing
from engine.shader import Shader
import glm

class Cube(Thing):
    def __init__(self, name: str, parent: Optional[Thing] = None, shader: Optional[Shader] = None) -> None:
        super().__init__(name, parent, shader)
        self.vertices = np.array([
            # positions         # colors
            -0.5, -0.5, -0.5,   1.0, 0.0, 0.0,
             0.5, -0.5, -0.5,   0.0, 1.0, 0.0,
             0.5,  0.5, -0.5,   0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5,   1.0, 1.0, 0.0,
            -0.5, -0.5,  0.5,   0.0, 1.0, 1.0,
             0.5, -0.5,  0.5,   1.0, 0.0, 1.0,
             0.5,  0.5,  0.5,   0.5, 0.5, 0.5,
            -0.5,  0.5,  0.5,   0.1, 0.2, 0.3,
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            0, 1, 5, 5, 4, 0,
            2, 3, 7, 7, 6, 2,
            0, 3, 7, 7, 4, 0,
            1, 2, 6, 6, 5, 1
        ], dtype=np.uint32)

        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * self.vertices.itemsize, None)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * self.vertices.itemsize, ctypes.c_void_p(3 * self.vertices.itemsize))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def render(self, view_matrix: glm.mat4, projection_matrix: glm.mat4) -> None:
        if self.shader:
            self.shader.use()
            model_matrix = self.get_model_matrix()
            model_loc = gl.glGetUniformLocation(self.shader.program, "model")
            view_loc = gl.glGetUniformLocation(self.shader.program, "view")
            projection_loc = gl.glGetUniformLocation(self.shader.program, "projection")

            gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, glm.value_ptr(model_matrix))
            gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, glm.value_ptr(view_matrix))
            gl.glUniformMatrix4fv(projection_loc, 1, gl.GL_FALSE, glm.value_ptr(projection_matrix))

        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, None)
        gl.glBindVertexArray(0)

        super().render(view_matrix, projection_matrix)
