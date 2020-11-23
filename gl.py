# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Using OpenGl
# Code based on Carlos Alonso (Professor Code)

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np
from obj import Obj



# # Defining a model of a cube with its vertex and indexes to connect
#                      # VERTS           COLOR
# rectVerts = np.array([ 0.5, 0.5, 0.5,  1,0,0, 
#                        0.5,-0.5, 0.5,  0,1,0, 
#                       -0.5,-0.5, 0.5,  0,0,1, 
#                       -0.5, 0.5, 0.5,  1,1,0,
#                        0.5, 0.5,-0.5,  1,0,1,
#                        0.5,-0.5,-0.5,  0,1,1,
#                       -0.5,-0.5,-0.5,  1,1,1,
#                       -0.5, 0.5,-0.5,  0,0,0 ], dtype=np.float32)

# rectIndices = np.array([ #front
#                          0, 1, 3,
#                          1, 2, 3,
#                          #left
#                          4, 5, 0,
#                          5, 1, 0,
#                          #back
#                          7, 6, 4,
#                          6, 5, 4,
#                          #right
#                          3, 2, 7,
#                          2, 6, 7,
#                          #top
#                          1, 5, 2,
#                          5, 6, 2,
#                          #bottom
#                          4, 0, 7,
#                          0, 3, 7], dtype=np.uint32)


class Model(object):
    def __init__(self, fileName, textureName, scale=glm.vec3(1,1,1),rotation=glm.vec3(0,0,0)):
        self.model = Obj(fileName)

        self.createVertBuffer()

        self.texture_surface = pygame.image.load(textureName)
        self.texture_data = pygame.image.tostring(self.texture_surface,"RGB",1)
        # print(self.texture_data)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0,0,0)
        self.rotation = rotation # pitch, yaw, roll
        self.scale = scale

    def getMatrix(self):
        i = glm.mat4(1)
        translate = glm.translate(i, self.position)
        pitch = glm.rotate(i, glm.radians( self.rotation.x ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( self.rotation.y ), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( self.rotation.z ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        return translate * rotate * scale

    def createVertBuffer(self):
        buffer = []

        for face in self.model.faces:
            for i in range(3):
                #verts
                buffer.append(self.model.vertices[face[i][0] - 1][0])
                buffer.append(self.model.vertices[face[i][0] - 1][1])
                buffer.append(self.model.vertices[face[i][0] - 1][2])
                buffer.append(1)

                #norms
                try:
                    buffer.append(self.model.normals[face[i][2] - 1][0])
                except:
                    buffer.append(0)
                try:
                    buffer.append(self.model.normals[face[i][2] - 1][1])
                except:
                    buffer.append(0)
                try:
                    buffer.append(self.model.normals[face[i][2] - 1][2])
                except:
                    buffer.append(0)
                buffer.append(0)

                #texcoords
                buffer.append(self.model.texcoords[face[i][1] - 1][0])
                buffer.append(self.model.texcoords[face[i][1] - 1][1])

        self.vertBuffer = np.array( buffer, dtype=np.float32)


    def renderInScene(self):
        try:
            VBO = glGenBuffers(1) #Vertex Buffer Object
            VAO = glGenVertexArrays(1) #Vertex Array Object

            glBindVertexArray(VAO)

            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW)

            # Atributo de posicion de vertices
            glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)

            # Atributo de normal de vertices
            glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 4))
            glEnableVertexAttribArray(1)

            ## Atributo de uvs de vertices
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 8))
            glEnableVertexAttribArray(2)

            # Dar textura
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture_surface.get_width(), self.texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)
        
        except Exception as e:
            print(e)



#Class Renderer to use function of OpenGl
class Renderer(object):
    #Init given a pygame screen
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        #Gl Enable as Depth and Create our Viewport
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        
        self.modelShow = 0

        self.modelList = []
        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)
        #Cam pos, cube pos and cam rotation
        self.camPos = glm.vec3(0,0,3)
        self.cubePos = glm.vec3(0,0,0)
        self.yawCam=0
        self.pitchCam =0
        self.rollCam =0

        # Light
        self.pointLight = glm.vec4(0,0,0,0)

        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

    def getViewMatrix(self):
        i = glm.mat4(1)
        
        # View Matrix and Translation
        camTranslate = glm.translate(i, self.camPos)
        camPitch = glm.rotate(i, glm.radians( self.pitchCam ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( self.yawCam), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( self.rollCam ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        view = glm.inverse( camTranslate * camRotate )
        
        return view
    
    def getLookAtMatrix(self,eye=(0,0,0)):
        view=glm.lookAt(glm.vec3(self.camPos.x, self.camPos.y, self.camPos.z), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0,1.0, 0.0))
        return view

    # Setting only wireframeMode with Gllines mode
    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Setting  filledMode with GlFill mode
    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #Translate Cube
    def translateCube(self, x, y, z):
        self.cubePos = glm.vec3(x,y,z)
    
    #Translate Camera
    def translateCamera(self, x, y, z):
        self.camPos = glm.vec3(x,y,z)
        # self.pointLight = glm.vec4(x,y,z,0)
    
    #Rotate Camera
    def rotateCamera(self, pitch,roll,yaw):
        self.yawCam = yaw
        self.pitchCam = pitch
        self.rollCam = roll

    #Setting active shaders by compilingShaders and then compiling them as a program
    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)



    # Render function that its called in a loop to render content on screen
    def render(self):
        glClearColor(0.4, 0.4, 0.4, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )


        
        

        #Check for any active shader
        if self.active_shader:

            
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr( self.getLookAtMatrix() ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr( self.projection ))
            
            glUniform4f(glGetUniformLocation(self.active_shader, "light"), 
                        self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)

            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 
                        1, 1, 1, 1)
            
            glUniform1f(glGetUniformLocation(self.active_shader, "time"), 
                        (pygame.time.get_ticks()/1000))
        #Draw all models on scene and bind Vertexes
        # for model in self.modelList:
        if(len(self.modelList)>0):
            model = self.modelList[self.modelShow]    
            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                                   1, GL_FALSE, glm.value_ptr( model.getMatrix() ))

            model.renderInScene()
