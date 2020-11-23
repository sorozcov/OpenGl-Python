# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Using OpenGl
# Code based on Carlos Alonso (Professor Code)

import pygame
from pygame.locals import *
from numpy import cos, sin,radians,abs
from gl import Renderer,Model
import shaders
import glm


pygame.init()

global closeExit
closeExit=False
#Init Pygame
pygame.init()
screenWidth=1000
screenHeight=500
pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play(-1)
#Main Menu Screen
def mainMenu():
    
    screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL ) #, pygame.FULLSCREEN)
    pygame.display.set_caption('OpenGl')
    
    #Background image
    bg = pygame.image.load("bg.jpg")
    screen.fill([247, 247, 247 ])
    rectangle=bg.get_rect()
    bg=pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    screen.blit(bg,((screen.get_width()-bg.get_width())/2,0))

    #Title of Screen
    font = pygame.font.SysFont("Arial", 40)
    title = str((" "*3+"OpenGl Project"+" "*3))
    title = font.render(title, 1, pygame.Color("black"))
    titleRec = title.get_rect()
    titleRec.center = (screen.get_width() // 2, screen.get_height() // 6) 
    screen.fill(pygame.Color("white"), titleRec)
    screen.blit(title, titleRec)

    #Button Start
    buttonStart = str((" "*3+"Start"+" "*3))
    buttonStart = font.render(buttonStart, 1, pygame.Color("black"))
    buttonStartRec = buttonStart.get_rect()
    buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
    screen.fill(pygame.Color("white"), buttonStartRec)
    screen.blit(buttonStart, buttonStartRec)

    #Button Quit
    buttonQuit = str((" "*3+"Quit"+" "*3))
    buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
    buttonQuitRec = buttonQuit.get_rect()
    buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
    screen.fill(pygame.Color("white"), buttonQuitRec)
    screen.blit(buttonQuit, buttonQuitRec)




    isRunning = True
    closeExit=False
    buttonPressed=None
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                closeExit = True
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                    closeExit = True
                elif ev.key == pygame.K_DOWN:
                    if(buttonPressed==buttonQuitRec):
                        bp=None
                    elif(buttonPressed==buttonStartRec):
                        bp=buttonQuitRec
                    elif(buttonPressed==None):
                        bp=buttonStartRec
                    
                    buttonPressed=bp
                elif ev.key == pygame.K_UP:
                    if(buttonPressed==buttonStartRec):
                        bp=None
                    elif(buttonPressed==buttonQuitRec):
                        bp=buttonStartRec
                    elif(buttonPressed==None):
                        bp=buttonQuitRec
                    buttonPressed=bp
                elif ev.key == pygame.K_RETURN:
                    if buttonPressed==buttonQuitRec: 
                        isRunning = False 
                        closeExit=True
                    elif buttonPressed==buttonStartRec: 
                        isRunning = False 
                        closeExit=False
                    

            #Check for mouse clicks
            elif ev.type == pygame.MOUSEBUTTONDOWN: 
                mouse = pygame.mouse.get_pos()
                
                #Button Quit
                if buttonQuitRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExit=True
                elif buttonStartRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExit=False
                else:
                    buttonPressed=None
            #Check for hovers on buttons
            mouse = pygame.mouse.get_pos()
            if buttonQuitRec.collidepoint(mouse) or buttonPressed==buttonQuitRec: 
                buttonPressed=buttonQuitRec
                buttonQuit = str((" "*3+"Quit"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("WHITE"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            else:
                
                buttonQuit = str((" "*3+"Quit"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("white"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            
            if buttonStartRec.collidepoint(mouse) or buttonPressed==buttonStartRec: 
                buttonPressed=buttonStartRec
                buttonStart = str((" "*3+"Start"+" "*3))
                buttonStart = font.render(buttonStart, 1, pygame.Color("white"))
                buttonStartRec = buttonStart.get_rect()
                buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonStartRec)
                screen.blit(buttonStart, buttonStartRec)
            else: 
                
                buttonStart = str((" "*3+"Start"+" "*3))
                buttonStart = font.render(buttonStart, 1, pygame.Color("black"))
                buttonStartRec = buttonStart.get_rect()
                buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("white"), buttonStartRec)
                screen.blit(buttonStart, buttonStartRec)
        pygame.display.update()
    
    #Start of our Real Raytracer
    if(not closeExit):
        render()
        






def render():
    # Initializr pygame and our own renderer based on OpenGl
    deltaTime = 0.0

    clock = pygame.time.Clock()
    screenSize = (960, 540)
    screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('OpenGl')
    
    renderer = Renderer(screen)
    # Set shaders and create objects
    renderer.setShaders(shaders.vertex_shader, shaders.fragment_shader)

    
    renderer.modelList.append(Model('tri_coca.obj', 'coca.png',glm.vec3(0.4,0.4,0.4)))
    renderer.modelList.append(Model('tri_hamster.obj', 'hamster.bmp',glm.vec3(3/4,3/4,3/4),glm.vec3(0,90,0)))
    renderer.modelList.append(Model('tri_R2.obj', 'R2.bmp',glm.vec3(1.5/3,1.5/3,1.5/3)))
    renderer.modelList.append(Model('tri_apple.obj', 'apple.jpg',glm.vec3(15,15,15)))
    renderer.modelList.append(Model('tri_heart.obj', 'heart.png',glm.vec3(7,7,7)))




    #Initial Camera Position and Rotation
    renderer.camPos = glm.vec3(0,0,10)
    cameraX,cameraY,cameraZ = renderer.camPos
    pitch = renderer.pitchCam
    yaw = renderer.yawCam
    roll = renderer.rollCam
    renderer.pointLight.z = 20
    #Check if we are tryng to render the screen
    isRendering = True
    radius = 10
    camAngle = 0;
    a=1
    while isRendering:

        # Check if any key is pressed
        keys = pygame.key.get_pressed()
        
        #Movement in camera X, camera Y and camera Z.
        # if keys[pygame.K_a]:
        #     cameraX -= 2 * deltaTime
        # if keys[pygame.K_d]:
        #     cameraX += 2 * deltaTime
        # if keys[pygame.K_e]:
        #     if(cameraZ>4):
        #         cameraZ -= 2 * deltaTime
        # if keys[pygame.K_q]:
        #     if(cameraZ<15):
        #         cameraZ += 2 * deltaTime
        # if keys[pygame.K_s]:
        #     cameraY -= 2 * deltaTime
        # if keys[pygame.K_w]:
        #     cameraY += 2 * deltaTime

        if keys[pygame.K_a]:
            camAngle -=1
            cameraX = sin(radians(camAngle)) * radius;
            cameraZ = cos(radians(camAngle)) * radius;
        if keys[pygame.K_d]:
            camAngle +=1
            cameraX = sin(radians(camAngle)) * radius;
            cameraZ = cos(radians(camAngle)) * radius;
        if keys[pygame.K_e]:
            if(radius>4):
                radius -= 2 * deltaTime
                cameraX = sin(radians(camAngle)) * radius;
                cameraZ = cos(radians(camAngle)) * radius;
        if keys[pygame.K_q]:
            if(radius<15):
                radius += 2 * deltaTime
                cameraX = sin(radians(camAngle)) * radius;
                cameraZ = cos(radians(camAngle)) * radius;
        if keys[pygame.K_s]:
            if(cameraY>=-radius):
                cameraY -= 5 * deltaTime  
        if keys[pygame.K_w]:
            if(cameraY<=radius):
                cameraY += 5 * deltaTime
        #Reset Camera to Default
        if keys[pygame.K_r]:
            cameraX=0
            cameraY=0
            cameraZ=10
            camAngle=0
            radius=10
        
        if(pygame.mouse.get_pressed()[0]==1):
            mouseMove = pygame.mouse.get_rel()
            if(mouseMove[0]!=0):
                camAngle += mouseMove[0]
                cameraX = sin(radians(camAngle)) * radius;
                cameraZ = cos(radians(camAngle)) * radius;
            elif(mouseMove[1]!=0):
                    if(mouseMove[1]>0):
                        nextCamY = cameraY + abs(mouseMove[1]*0.2)
                        if(not nextCamY>=radius):
                            cameraY = nextCamY
                    else:
                        nextCamY = cameraY - abs(mouseMove[1]*0.2)
                        if(not nextCamY<=-radius):
                            cameraY = nextCamY

        # #Rotation in camera
        # if keys[pygame.K_i]:
        #     pitch -= 10 * deltaTime
        # if keys[pygame.K_o]:
        #     pitch += 10 * deltaTime
        # if keys[pygame.K_k]:
        #     yaw -= 10 * deltaTime
        # if keys[pygame.K_l]:
        #     yaw += 10 * deltaTime
        # if keys[pygame.K_j]:
        #     roll -= 10 * deltaTime
        # if keys[pygame.K_h]:
        #     roll += 10 * deltaTime


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
                #Change object
                elif ev.key == pygame.K_SPACE:
                    renderer.modelShow = (renderer.modelShow + 1) % len(renderer.modelList)
                    if(renderer.modelShow==4):
                        pygame.mixer.music.load("heartbeat.mp3")
                        pygame.mixer.music.play(-1)
                        # heart_shader didnt work:(
                        renderer.setShaders(shaders.vertex_shader, shaders.fragment_shader)
                    elif((renderer.modelShow==0)):
                        pygame.mixer.music.load("bgmusic.mp3")
                        pygame.mixer.music.play(-1)
                        renderer.setShaders(shaders.vertex_shader, shaders.fragment_shader)
                elif ev.key == pygame.K_ESCAPE:
                    isRendering = False
            #Mouse Movement
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 3:
                    #Reset cam pos
                    cameraX=0
                    cameraY=0
                    cameraZ=10
                    camAngle=0
                    radius=10
                elif ev.button == 4:
                    if(radius>4):
                        radius -= 10 * deltaTime
                        cameraX = sin(radians(camAngle)) * radius;
                        cameraZ = cos(radians(camAngle)) * radius;
                elif ev.button == 5:
                    if(radius<15):
                        radius += 10 * deltaTime
                        cameraX = sin(radians(camAngle)) * radius;
                        cameraZ = cos(radians(camAngle)) * radius;
            


        # Traslate and rotate our camera
        renderer.translateCamera(cameraX,cameraY,cameraZ)
        renderer.rotateCamera(pitch,yaw,roll)

        # Render loop
        try:
            renderer.render()
        except Exception as e:
            print(e)
        pygame.display.flip()
        clock.tick(60)
        deltaTime = clock.get_time() / 1000

mainMenu()
pygame.mixer.music.stop()
pygame.quit()
