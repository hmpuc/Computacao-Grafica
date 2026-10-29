# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

import platform
import os

# Se for no Windows, inclua o diretorio atual no path
if platform.system() == 'Windows':
    CWD = os.getcwd()
    os.add_dll_directory(CWD)

import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ListaDeCoresRGB import *
from Poligono import *


# Modelos de Objetos
MeiaSeta = Poligono()
Mastro = Poligono()

Poly = Poligono()

PontoClicado = Ponto()
FoiClicado = False

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# define uma funcao de limpeza de tela
from os import system, name
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        print("*******************")
        print ("PWD: ", os.getcwd()) 

def init():

    global Min, Max

    # Define a cor do fundo da tela (AZUL)
    glClearColor(0.0, 0.0, 1.0, 1.0)

    Min = Ponto (-20, -20)
    Max = Ponto (20, 20)
    
    Poly.LePoligono("Retangulo1x1.txt")

# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizacao da tela em 30s
        AccumDeltaT = 0
        glutPostRedisplay()
    if TempoTotal > 5.0:
        print ("Tempo Acumulado: ", TempoTotal," segundos. ")
        print ("Nros de Frames sem desenho: ", nFrames)
        print ("FPS(sem desenho): ", nFrames/TempoTotal)
        TempoTotal = 0;
        nFrames = 0;


def reshape(w: int, h: int):
    
    global Min, Max

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Define a area a ser ocupada pela area OpenGL dentro da Janela
    glViewport(0, 0, w, h)

    # Define os limites logicos da area OpenGL dentro da Janela
    Min.imprime("Minimo: ")
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


# **********************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ****************************************************************
def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)

# **************************************************************
def DesenhaEixos():
    global Min, Max

    Meio = Ponto()
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
    glEnd()


def square():
    glBegin(GL_QUADS)
    glVertex2f(10, 10)
    glVertex2f(15, 10)
    glVertex2f(15, 15)
    glVertex2f(10, 15)
    glEnd()


# ***********************************************************************************
def DesenhaTriangulo(A: Ponto, B:Ponto, C:Ponto):
    glBegin(GL_TRIANGLES)
    glVertex2f(A.x, A.y)
    glVertex2f(B.x, B.y)
    glVertex2f(C.x, C.y)
    glEnd()

def display():
    # Limpa a tela com a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	# Coloque aqui as chamadas das rotinas que desenham os objetos
	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    defineCor(GreenYellow)

    P1 = Ponto
    P1 = Ponto(-10,-10)
    P2 = Ponto 
    P2 = Ponto(0, 10)
    P3 = Ponto
    P3 = Ponto(10, -10)
    
    glPushMatrix()
    DesenhaTriangulo(P1, P2, P3)
    glPopMatrix()

    glLineWidth(4)
    glColor3f(1,1,1) # R, G, B  [0..1]
    DesenhaEixos()
    
    defineCor(IndianRed)
    Poly.desenhaPoligono()



    glutSwapBuffers()



# **********************************************************************
# The function called whenever a key is pressed. 
# # Note the use of Python tuples to pass in: (key, x, y)
# 
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    if (button != GLUT_LEFT_BUTTON):
        print ("Botao Esquerdo - Mouse :", x, ",", y)

    # vport = glGetIntegerv(GL_VIEWPORT)
    # realY = vport[3] - y
    # mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    # projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    
    # worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    # print ("Ponto: ", worldCoordinate1)
    
    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)

glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)

# Cria a janela na tela, definindo o nome da
# que aparecera na barra de titulo da janela.
glutInitWindowPosition(100, 100)

wind = glutCreateWindow(b"Programa Basico OpenGL")

# executa algumas inicializacoes
init ()


# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serah chamada automaticamente quando
# for necessario redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serah chamada automaticamente quando
# o usuaio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serah chamada automaticamente sempre
# o usuario pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)

try:
	glutMainLoop()
except SystemExit:
	pass
