import glm

class Camera:
    def __init__(self, position: glm.vec3, target: glm.vec3, up: glm.vec3, fov: float, aspect_ratio: float, near: float, far: float) -> None:
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far

    def get_view_matrix(self) -> glm.mat4:
        return glm.lookAt(self.position, self.target, self.up)

    def get_projection_matrix(self) -> glm.mat4:
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)