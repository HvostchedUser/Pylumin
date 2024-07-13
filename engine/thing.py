from typing import List, Optional, Dict, Any
import glm
from engine.shader import Shader

class Thing:
    def __init__(self, name: str, parent: Optional['Thing'] = None, shader: Optional[Shader] = None) -> None:
        self.name = name
        self.parent = parent
        self.children: List['Thing'] = []
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.quat()
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.shader = shader
        self.uniforms: Dict[str, Any] = {}
        if parent:
            parent.add_child(self)

    def add_child(self, child: 'Thing') -> None:
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'Thing') -> None:
        self.children.remove(child)
        child.parent = None

    def get_model_matrix(self) -> glm.mat4:
        translate_matrix = glm.translate(glm.mat4(1.0), self.position)
        rotate_matrix = glm.mat4_cast(self.rotation)
        scale_matrix = glm.scale(glm.mat4(1.0), self.scale)
        model_matrix = translate_matrix * rotate_matrix * scale_matrix
        if self.parent:
            model_matrix = self.parent.get_model_matrix() * model_matrix
        return model_matrix

    def set_position(self, position: glm.vec3) -> None:
        self.position = position

    def set_rotation(self, rotation: glm.quat) -> None:
        self.rotation = rotation

    def set_scale(self, scale: glm.vec3) -> None:
        self.scale = scale

    def set_uniform(self, name: str, value: Any) -> None:
        self.uniforms[name] = value

    def update(self, delta_time: float) -> None:
        for child in self.children:
            child.update(delta_time)

    def render(self, view_matrix: glm.mat4, projection_matrix: glm.mat4) -> None:
        if self.shader:
            self.shader.use()
            model_matrix = self.get_model_matrix()
            self.shader.set_uniform("model", model_matrix)
            self.shader.set_uniform("view", view_matrix)
            self.shader.set_uniform("projection", projection_matrix)

            for name, value in self.uniforms.items():
                self.shader.set_uniform(name, value)


        for child in self.children:
            child.render(view_matrix, projection_matrix)
