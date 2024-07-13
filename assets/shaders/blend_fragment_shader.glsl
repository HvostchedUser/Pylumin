#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D layer1Texture;
uniform sampler2D layer2Texture;
uniform sampler2D layer3Texture;

void main()
{
    vec4 color1 = texture(layer1Texture, TexCoords);
    vec4 color2 = texture(layer2Texture, TexCoords);
    vec4 color3 = texture(layer3Texture, TexCoords);

    // Blend the layers based on their alpha values
    vec4 blendedColor = color1 + (1.0 - color1.a) * color2 + (1.0 - color1.a) * (1.0 - color2.a) * color3;
    FragColor = blendedColor;
}
