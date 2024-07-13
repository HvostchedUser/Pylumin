#version 330 core
out vec4 FragColor;

in vec3 ourColor;

void main()
{
    // Invert the colors for demonstration purposes
    FragColor = vec4(1.0 - ourColor, 1.0);
}
