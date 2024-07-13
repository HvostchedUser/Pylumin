from typing import List
import OpenGL.GL as gl
import glm

class Scene:
    def __init__(self) -> None:
        self.things: List['Thing'] = []

    def add_thing(self, thing: 'Thing') -> None:
        self.things.append(thing)

    def remove_thing(self, thing: 'Thing') -> None:
        self.things.remove(thing)

    def update(self, delta_time: float) -> None:
        for thing in self.things:
            thing.update(delta_time)

    def render(self, camera: 'Camera') -> None:
        for thing in self.things:
            thing.render(camera)

class Renderer:
    def __init__(self) -> None:
        pass  # Initialize OpenGL context, setup viewport, etc.

    def render_scene(self, scene: Scene, camera: 'Camera') -> None:
        view_matrix = camera.get_view_matrix()
        projection_matrix = camera.get_projection_matrix()

        for thing in scene.things:
            thing.render(view_matrix, projection_matrix)
