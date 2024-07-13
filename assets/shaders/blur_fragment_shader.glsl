#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;

const float offset = 1.0 / 300.0; // Adjust according to texture resolution
const float alpha_threshold = 0.1; // Threshold to discard low alpha values

void main()
{
    vec4 color = vec4(0.0);
    for (int x = -5; x <= 5; ++x)
    {
        for (int y = -5; y <= 5; ++y)
        {
            vec2 offsetCoords = vec2(TexCoords.x + x * offset, TexCoords.y + y * offset);
            color += texture(screenTexture, offsetCoords);
        }
    }
    color /= 121.0; // Normalize color
    if (color.a < alpha_threshold)
    {
        discard; // Discard low alpha pixels
    }
    FragColor = color;
}
