#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

void main()
{
    vec3 position = aPos;
    position.x += sin(time*10 + aPos.y * 10.0) * 0.5;
    position.y += cos(time*10 + aPos.x * 10.0) * 0.5;

    gl_Position = projection * view * model * vec4(position, 1.0);
    ourColor = aColor;
}
