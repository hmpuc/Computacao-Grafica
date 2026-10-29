# ***********************************************************************************
#   OpenGLBasico3D-V8-Exercicios.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#       Adaptação: Gabriel Fonseca Silva
#       fonseca.gabriel@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
#
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
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
#
# ***********************************************************************************
import os
import sys

# Em alguns sistemas Linux, pode ser necessário comentar este bloco ou
# trocar "glx" pelo backend OpenGL disponível na máquina.
if sys.platform.startswith("linux"):
    os.environ.setdefault("PYOPENGL_PLATFORM", "glx")

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ListaDeCoresRGB import *
import time
import random as ALE


# EXERCÍCIOS — CÂMERA E PROJEÇÕES
# Os controles descritos nos TODOs são sugestões A IMPLEMENTAR.
#
# Exercício 1: posição do observador e direção de visão (eye e center).
# Exercício 2: parâmetros da perspectiva (FOV, near e far).
# Exercício 3: parâmetros da ortográfica (left, right, bottom, top, near, far).
# Exercício 4: alternância de projeção, restauração e consulta dos parâmetros.
# Cada TODO X.Y pertence ao exercício X; Y identifica a etapa.
#
# EXTRA (opcional): câmera orbital em torno de um ponto focal móvel.
# A câmera orbital não faz parte dos TODOs obrigatórios desta versão.
#

eye = [10,0,10]
center = [0,0,0]
up = [0,2,0]

fov = 120
near = 0.01
far = 50
# TODO 3.1: Criar left=-10, right=10, bottom=-10 e top=10.
# Compartilhar near/far com a perspectiva para simplificar a alternância.
#
# TODO 4.1: Criar uma variável para a projeção ativa (inicial: perspectiva).
# Guardar os valores iniciais da câmera e das projeções para restaurá-los.
# Se usar listas, guardar cópias independentes do estado que será alterado.
#
AspectRatio = 1.0
AnimacaoAtiva = True
Angulo = 0.0
# **********************************************************************
#  init()
#  Inicializa os parâmetros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (cinza)
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
    # Evita dimensões nulas ao minimizar ou redimensionar a janela.
    w = max(w, 1)
    h = max(h, 1)
    # Ajusta a relacao entre largura e altura para evitar distorcao na imagem.
    # Veja funcao "PosicUser".
    AspectRatio = w / h
    # Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)

    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4]
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0, 1.0]  # Posição da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0


    #Habilita o uso de iluminação
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz numero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentração do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado será o brilho. (Valores válidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)

# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCubo():
    glutSolidCube(2)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # TODO 3.2: Implementar glOrtho(left, right, bottom, top, near, far).
    # Validar left < right e bottom < top; neste exercício, manter também
    # 0 < near < far nas duas projeções, por conveniência.
    # TODO 4.2: Escolher UMA projeção conforme o modo ativo, após o reset
    # da matriz. Alternar a projeção não deve alterar eye ou center.
    if fov <= 0:
        print("Fov não pode ser menor ou igual a 0")
    if fov > 180:
        print("Fov não pode ser maior ou igual a 180")
    if near < 0:
        print("Near não pode ser menor que 0")
    if near > far:
        print("Far não pode ser menor que near")
    gluPerspective(fov, AspectRatio, near, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma célula do piso.
# O ladrilho tem largura 1, centro no (0,0,0) e está sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho(corBorda, corDentro):
    SetColor(corDentro)
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()


    SetColor(corBorda)
    glLineWidth(3)
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()
    glLineWidth(1)

# **********************************************************************
def DesenhaPiso():
    ALE.seed(0) # Usa uma semente fixa para gerar sempre as mesmas cores no piso
    glPushMatrix()
    glTranslated(-20,-1,-10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho(White, ALE.randint(0, 30))
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    PosicUser()
    DefineLuz()  # Luz posicionada no mundo após configurar a câmera.
    glMatrixMode(GL_MODELVIEW)


    glPushMatrix()
    glColor3f(1,0.0,0.0) # Vermelho
    glTranslatef(5,0,3)
    glRotatef(Angulo,0,1,0)
    DesenhaCubo()
    glPopMatrix()

    glColor3f(0.6156862745, 0.8980392157, 0.9803921569) # Azul
    glPushMatrix()
    glTranslatef(-4,0,2)
    glRotatef(Angulo,0,1,0)
    DesenhaCubo()
    glPopMatrix()

    DesenhaPiso()


    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Atualiza a animação pelo tempo decorrido e solicita redesenhos.
#
# **********************************************************************
# Variaveis Globais
AccumDeltaT = 0
oldTime = time.time()

def animate():
    global AccumDeltaT, oldTime, Angulo

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime
    if AnimacaoAtiva:
        Angulo = (Angulo + 60.0 * dt) % 360.0

    AccumDeltaT += dt

    if AccumDeltaT > 1.0/30:  # fixa a atualização da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()


# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(key, x, y):
    global AnimacaoAtiva
    global eye
    global center
    global far
    global near
    global fov
    if key == ESCAPE:
        os._exit(0)
    if key == b' ':
        AnimacaoAtiva = not AnimacaoAtiva

    if key == b'w':
        eye[2] -= 1
    if key == b's':
        eye[2] += 1
    if key == b'a':
        eye[0] -= 1
    if key == b'd':
        eye[0] += 1
    if key == b'q':
        eye[1] -= 1
    if key == b'e':
        eye[1] += 1

    if key == b'i':
        center[2] -= 1
    if key == b'k':
        center[2] += 1
    if key == b'j':
        center[0] -= 1
    if key == b'l':
        center[0] += 1
    if key == b'u':
        center[1] -= 1
    if key == b'o':
        center[1] += 1

    # TODO 2.3: Usar [ / ] para diminuir/aumentar FOV,
    # 1 / 2 para near e 3 / 4 para far. Definir passos adequados e validar.
    # Comparar diminuir FOV com aproximar eye: observar também o piso.
    # Produzir um recorte parcial de um cubo alterando near/far.
    if key == b'1':
        if (near - 0.05 >= 0.01):
            near -= 0.05
    if key == b'2':
        if (near + 0.5 < far):
            near += 0.5
    if key == b'3':
        if (far - 0.5 > near):
            far -= 0.5
    if key == b'4':
        far += 0.5
    if fov == b'[':
        if (pov - 1 > 0):
            pov -= 1
    if fov == b']':
        if (pov + 1 < 180):
            pov += 1

    # TODO 3.3: Controlar cada limite ortográfico independentemente:
    # 5 / 6: left; 7 / 8: right; 9 / 0: bottom; - / =: top.
    # Cada par diminui/aumenta o parâmetro. Near/far usam 1/2 e 3/4.
    # Aplicar esses controles de limites apenas no modo ortográfico.
    # Observar: reduzir a extensão do volume amplia a imagem dos objetos.

    # TODO 4.3: Usar p para alternar perspectiva/ortográfica; r para
    # restaurar câmera e projeções; v para imprimir modo e parâmetros.
    # Imprimir também a lista dos controles implementados.
    # TODO 4.4: Comparar as projeções com a mesma câmera e redimensionar
    # a janela. Explicar o efeito da razão (right-left)/(top-bottom)
    # quando ela difere de AspectRatio na projeção ortográfica.

    glutPostRedisplay()

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
# Programa Principal
# ***********************************************************************************


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(700, 700)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de título da janela.
glutInitWindowPosition(100, 100)
glutCreateWindow(b"OpenGL 3D - Exercicios de camera")

# executa algumas inicializações
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# será chamada automaticamente quando
# for necessário redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# será chamada automaticamente quando
# o usuário alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# será chamada automaticamente sempre
# o usuário pressionar uma tecla comum
glutKeyboardFunc(keyboard)

# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" será chamada
# automaticamente sempre o usuário
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
