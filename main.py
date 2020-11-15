# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Using OpenGl
# Code based on Carlos Alonso (Professor Code)

import pygame
from pygame.locals import *
from gl import Renderer
import shaders


# Initializr pygame and our own renderer based on OpenGl
deltaTime = 0.0
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)


renderer = Renderer(screen)
# Set shaders and create objects
renderer.setShaders(shaders.vertex_shader, shaders.fragment_shader)
renderer.createObjects()


#Initial Camera Position and Rotation
cameraX,cameraY,cameraZ = renderer.camPos
pitch = renderer.pitchCam
yaw = renderer.yawCam
roll = renderer.rollCam

#Check if we are tryng to render the screen
isRendering = True
while isRendering:

    # Check if any key is pressed
    keys = pygame.key.get_pressed()
    #Movement in camera X, camera Y and camera Z.
    if keys[pygame.K_a]:
        cameraX -= 2 * deltaTime
    if keys[pygame.K_d]:
        cameraX += 2 * deltaTime
    if keys[pygame.K_e]:
        cameraZ -= 2 * deltaTime
    if keys[pygame.K_q]:
        cameraZ += 2 * deltaTime
    if keys[pygame.K_s]:
        cameraY -= 2 * deltaTime
    if keys[pygame.K_w]:
        cameraY += 2 * deltaTime
    #Rotation in camera
    if keys[pygame.K_i]:
        pitch -= 10 * deltaTime
    if keys[pygame.K_o]:
        pitch += 10 * deltaTime
    if keys[pygame.K_k]:
        yaw -= 10 * deltaTime
    if keys[pygame.K_l]:
        yaw += 10 * deltaTime
    if keys[pygame.K_j]:
        roll -= 10 * deltaTime
    if keys[pygame.K_h]:
        roll += 10 * deltaTime


    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRendering = False
        elif ev.type == pygame.KEYDOWN:
            # Checking for any other key pressed to exit
            #Filled Mode
            if ev.key == pygame.K_1:
                renderer.filledMode()
            #WireframeMode
            elif ev.key == pygame.K_2:
                renderer.wireframeMode()
            elif ev.key == pygame.K_ESCAPE:
                isRendering = False


    # Traslate and rotate our camera
    renderer.translateCamera(cameraX,cameraY,cameraZ)
    renderer.rotateCamera(pitch,yaw,roll)

    # Render loop
    renderer.render()
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000


pygame.quit()
