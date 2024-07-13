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
from engine.magic import Scene, Renderer
from engine.shader import Shader
from engine.framebuffer import Framebuffer
from engine.quad_renderer import QuadRenderer

def initialize_scene() -> Tuple[Scene, Camera, Cube]:
    # Load shaders
    shader1 = Shader('assets/shaders/vertex_shader.glsl', 'assets/shaders/fragment_shader.glsl')
    shader2 = Shader('assets/shaders/vertex_shader_2.glsl', 'assets/shaders/fragment_shader_2.glsl')

    # Create scene
    scene = Scene()

    # Create Things
    parent_thing = Cube('Parent', shader=shader1)
    child_thing = Cube('Child', parent=parent_thing, shader=shader2)
    child_thing.set_position(glm.vec3(1.5, 0.0, 0.0))
    child_thing.set_uniform('time', 0.0)  # Initialize with 0.0
    scene.add_thing(parent_thing)

    # Create Camera
    camera = Camera(
        position=glm.vec3(3.0, 3.0, 3.0),
        target=glm.vec3(0.0, 0.0, 0.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        fov=90.0,
        aspect_ratio=800 / 600,
        near=0.1,
        far=100.0
    )

    return scene, camera, child_thing

def main() -> None:
    window_size: Tuple[int, int] = (800, 600)
    pygame.init()
    pygame.display.set_caption('Pylumin')
    pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    gl.glEnable(gl.GL_DEPTH_TEST)

    scene, camera, child_thing = initialize_scene()
    renderer = Renderer()
    framebuffer = Framebuffer(window_size[0], window_size[1])
    quad_renderer = QuadRenderer()
    blur_shader = Shader('assets/shaders/blur_vertex_shader.glsl', 'assets/shaders/blur_fragment_shader.glsl')

    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        delta_time: float = clock.tick() / 1000.0
        current_time = time.time() - start_time

        # Update transformations
        for thing in scene.things:
            thing.rotation = glm.rotate(thing.rotation, glm.radians(45 * delta_time), glm.vec3(0.0, 1.0, 0.0))
        child_thing.rotation = glm.rotate(child_thing.rotation, glm.radians(-45 * delta_time), glm.vec3(1.0, 0.0, 0.0))

        # Update scene
        scene.update(delta_time)

        # Update uniform for time
        child_thing.set_uniform('time', current_time)

        # Render to framebuffer
        framebuffer.bind()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        renderer.render_scene(scene, camera)
        framebuffer.unbind()

        # Apply blur shader
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        blur_shader.use()
        gl.glBindTexture(gl.GL_TEXTURE_2D, framebuffer.texture)
        quad_renderer.render()
        pygame.display.flip()

    framebuffer.cleanup()
    quad_renderer.cleanup()
    pygame.quit()

if __name__ == '__main__':
    main()
