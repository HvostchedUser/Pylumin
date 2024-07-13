#version 330 core
out vec4 FragColor;

in vec3 ourColor;

void main()
{
    vec3 glowColor = vec3(1.0, 1.0, 0.0); // Yellow color
    float distance = length(gl_PointCoord - vec2(0.5));
    float intensity = 1.0 - smoothstep(0.3, 0.5, distance);
    vec3 finalColor = mix(ourColor, glowColor, intensity);
    FragColor = vec4(finalColor, 1.0);
}
