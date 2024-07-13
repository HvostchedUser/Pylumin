#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;

const float offset = 1.0 / 300.0; // Adjust according to texture resolution

void main()
{
    vec3 result = vec3(0.0);
    for (int x = -2; x <= 2; ++x)
    {
        for (int y = -2; y <= 2; ++y)
        {
            vec2 offsetCoords = vec2(TexCoords.x + x * offset, TexCoords.y + y * offset);
            result += texture(screenTexture, offsetCoords).rgb;
        }
    }
    FragColor = vec4(result / 25.0, 1.0); // 25 is the kernel size (5x5)
}
