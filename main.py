import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import time
from typing import Tuple
import pygame
from pygame.locals import *
import OpenGL.GL as gl
import glm
from engine.eyes import Camera
from engine.kinds_of_things import Cube
from engine.scene import Scene
from engine.shader import Shader
from engine.layer import Layer
from engine.quad_renderer import QuadRenderer

def main() -> None:
    window_size: Tuple[int, int] = (800, 600)
    pygame.init()
    pygame.display.set_caption('Pylumin')
    pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # Load shaders
    blend_shader = Shader('assets/shaders/blend_vertex_shader.glsl', 'assets/shaders/blend_fragment_shader.glsl')


    shader1 = Shader('assets/shaders/vertex_shader.glsl', 'assets/shaders/fragment_shader.glsl')
    shader2 = Shader('assets/shaders/vertex_shader_2.glsl', 'assets/shaders/fragment_shader_2.glsl')
    blur_shader = Shader('assets/shaders/blur_vertex_shader.glsl', 'assets/shaders/blur_fragment_shader.glsl')
    pass_through_shader = Shader('assets/shaders/pass_through_vertex_shader.glsl',
                                 'assets/shaders/pass_through_fragment_shader.glsl')

    # Create scene
    scene = Scene(blend_shader)

    # Create layers with multisampling
    layer1 = Layer(window_size[0], window_size[1], blur_shader)
    layer2 = Layer(window_size[0], window_size[1], blur_shader)
    layer3 = Layer(window_size[0], window_size[1], blur_shader)

    # Create Things and add them to layers
    parent_thing = Cube(shader=shader1)
    child_thing = Cube(parent=parent_thing, shader=shader2)
    child_thing.set_position(glm.vec3(1.5, 0.0, 0.0))
    child_thing.set_uniform('time', 0.0)  # Initialize with 0.0
    cchild_thing = Cube(parent=child_thing, shader=shader1)
    cchild_thing.set_position(glm.vec3(1.5, 0.0, 0.0))

    layer1.add_thing(parent_thing)
    layer2.add_thing(child_thing)
    layer3.add_thing(cchild_thing)

    # Add layers to scene
    scene.add_layer(layer1)
    scene.add_layer(layer2)
    scene.add_layer(layer3)

    # Create Camera
    camera = Camera(
        position=glm.vec3(3.0, 3.0, 3.0),
        target=glm.vec3(0.0, 0.0, 0.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        fov=90.0,
        aspect_ratio=window_size[0] / window_size[1],
        near=0.1,
        far=100.0
    )

    quad_renderer = QuadRenderer()

    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        delta_time: float = clock.tick() / 1000.0
        current_time = time.time() - start_time

        parent_thing.rotation = glm.rotate(parent_thing.rotation, glm.radians(45 * delta_time), glm.vec3(0.0, 1.0, 0.0))
        child_thing.rotation = glm.rotate(child_thing.rotation, glm.radians(-45 * delta_time), glm.vec3(1.0, 0.0, 0.0))

        child_thing.set_uniform('time', current_time)

        # Render scene with layers
        scene.render(camera, quad_renderer)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
