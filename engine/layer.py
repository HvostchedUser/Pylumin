import OpenGL.GL as gl
from typing import List
from engine.framebuffer import Framebuffer
from engine.shader import Shader
from engine.thing import Thing
import glm

class Layer:
    def __init__(self, width: int, height: int, shader: Shader) -> None:
        self.width = width
        self.height = height
        self.shader = shader
        self.things: List[Thing] = []
        self.framebuffer = Framebuffer(width, height)

    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

    def remove_thing(self, thing: Thing) -> None:
        self.things.remove(thing)

    def render(self, camera: 'Camera') -> None:
        self.framebuffer.bind()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        view_matrix = camera.get_view_matrix()
        projection_matrix = camera.get_projection_matrix()

        for thing in self.things:
            thing.render(view_matrix, projection_matrix)

        self.framebuffer.unbind()

    def apply_shader(self, quad_renderer: 'QuadRenderer') -> None:
        self.framebuffer.bind()
        gl.glClearColor(0,0,0,0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.shader.use()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.framebuffer.texture)
        quad_renderer.render()
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        self.framebuffer.unbind()
