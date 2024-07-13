from typing import Any, Dict
import OpenGL.GL as gl
import glm

class Shader:
    def __init__(self, vertex_path: str, fragment_path: str) -> None:
        self.vertex_path = vertex_path
        self.fragment_path = fragment_path
        self.program = self.create_shader_program()

    def create_shader_program(self) -> int:
        vertex_shader = self.load_shader(self.vertex_path, gl.GL_VERTEX_SHADER)
        fragment_shader = self.load_shader(self.fragment_path, gl.GL_FRAGMENT_SHADER)
        program = gl.glCreateProgram()
        gl.glAttachShader(program, vertex_shader)
        gl.glAttachShader(program, fragment_shader)
        gl.glLinkProgram(program)
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            info_log = gl.glGetProgramInfoLog(program)
            gl.glDeleteProgram(program)
            raise RuntimeError(f'Shader link error: {info_log}')
        return program

    def load_shader(self, path: str, shader_type: int) -> int:
        with open(path, 'r') as file:
            source = file.read()
        shader = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)
        if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
            info_log = gl.glGetShaderInfoLog(shader)
            gl.glDeleteShader(shader)
            raise RuntimeError(f'Shader compile error ({path}): {info_log}')
        return shader

    def use(self) -> None:
        gl.glUseProgram(self.program)

    def set_uniform(self, name: str, value: Any) -> None:
        location = gl.glGetUniformLocation(self.program, name)
        if location == -1:
            raise ValueError(f"Uniform {name} not found in shader")

        if isinstance(value, float):
            gl.glUniform1f(location, value)
        elif isinstance(value, int):
            gl.glUniform1i(location, value)
        elif isinstance(value, glm.vec3):
            gl.glUniform3fv(location, 1, glm.value_ptr(value))
        elif isinstance(value, glm.mat4):
            gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(value))
        else:
            raise TypeError(f"Type of {name} not supported for uniform setting")
