# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Using OpenGl
# Code based on Carlos Alonso (Professor Code)

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np



# Defining a model of a cube with its vertex and indexes to connect
                     # VERTS           COLOR
rectVerts = np.array([ 0.5, 0.5, 0.5,  1,0,0, 
                       0.5,-0.5, 0.5,  0,1,0, 
                      -0.5,-0.5, 0.5,  0,0,1, 
                      -0.5, 0.5, 0.5,  1,1,0,
                       0.5, 0.5,-0.5,  1,0,1,
                       0.5,-0.5,-0.5,  0,1,1,
                      -0.5,-0.5,-0.5,  1,1,1,
                      -0.5, 0.5,-0.5,  0,0,0 ], dtype=np.float32)

rectIndices = np.array([ #front
                         0, 1, 3,
                         1, 2, 3,
                         #left
                         4, 5, 0,
                         5, 1, 0,
                         #back
                         7, 6, 4,
                         6, 5, 4,
                         #right
                         3, 2, 7,
                         2, 6, 7,
                         #top
                         1, 5, 2,
                         5, 6, 2,
                         #bottom
                         4, 0, 7,
                         0, 3, 7], dtype=np.uint32)




#Class Renderer to use function of OpenGl
class Renderer(object):
    #Init given a pygame screen
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        #Gl Enable as Depth and Create our Viewport
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)
        #Cam pos, cube pos and cam rotation
        self.camPos = glm.vec3(0,0,3)
        self.cubePos = glm.vec3(0,0,0)
        self.yawCam=0
        self.pitchCam =0
        self.rollCam =0

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

    #Creating objects (Right now only the cube)
    def createObjects(self):

        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.EBO = glGenBuffers(1) #Element Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, rectVerts.nbytes, rectVerts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectIndices.nbytes, rectIndices, GL_STATIC_DRAW)

        # Pointer reference to pos vertex
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Pointer reference to color vertex
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)


    # Render function that its called in a loop to render content on screen
    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        i = glm.mat4(1)
        # Model/Object matrix: translate * rotate * scale cUBE
        translate = glm.translate(i, self.cubePos)
        pitch = glm.rotate(i, glm.radians( 0 ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( 0), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, glm.vec3(1,1,1))
        model = translate * rotate * scale
        
        # View Matrix and Translation
        camTranslate = glm.translate(i, self.camPos)
        camPitch = glm.rotate(i, glm.radians( self.pitchCam ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( self.yawCam), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( self.rollCam ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        view = glm.inverse( camTranslate * camRotate )

        #Check for any active shader
        if self.active_shader:

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                               1, GL_FALSE, glm.value_ptr( model ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr( view ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr( self.projection ))

        #Draw all elments on scene and bind Vertexes
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
