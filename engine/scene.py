import OpenGL.GL as gl
from typing import List
from engine.layer import Layer
from engine.shader import Shader
from engine.quad_renderer import QuadRenderer

class Scene:
    def __init__(self, blend_shader) -> None:
        self.layers: List[Layer] = []
        self.blend_shader = blend_shader

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def remove_layer(self, layer: Layer) -> None:
        self.layers.remove(layer)

    def render(self, camera: 'Camera', quad_renderer: 'QuadRenderer') -> None:
        # Render each layer into its framebuffer
        for layer in self.layers:
            layer.render(camera)
            # layer.apply_shader(quad_renderer)

        # Render each layer's framebuffer texture to the screen using the blend shader
        gl.glClearColor(0,0,0,0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.blend_shader.use()

        for i, layer in enumerate(self.layers):
            gl.glActiveTexture(gl.GL_TEXTURE0 + i)
            gl.glBindTexture(gl.GL_TEXTURE_2D, layer.framebuffer.texture)
            self.blend_shader.set_uniform(f'layer{i+1}Texture', i)

        quad_renderer.render()

        for i in range(len(self.layers)):
            gl.glActiveTexture(gl.GL_TEXTURE0 + i)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)