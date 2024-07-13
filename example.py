import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np

# Initialization
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glOrtho(-2, 2, -1.5, 1.5, -1, 1)

# Set clear color to black
glClearColor(0.0, 0.0, 0.0, 1.0)

# Set point size
glPointSize(10.0)

# Set color to white
glColor3f(1.0, 1.0, 1.0)

# Vertex data
points = np.array([
    -1.0, -1.0, 0.0,
     1.0, -1.0, 0.0,
     0.0,  1.0, 0.0
], dtype=np.float32)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Renderg
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw points using glDrawArrays
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, points)
    glDrawArrays(GL_POINTS, 0, len(points)//3)
    glDisableClientState(GL_VERTEX_ARRAY)

    pygame.display.flip()
    pygame.time.wait(10)