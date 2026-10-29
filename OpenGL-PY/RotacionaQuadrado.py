import math
import time

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Classe que representa um ponto 2D, com operações úteis para movimentação
class Ponto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self) -> None:
        print("Ponto (", self.x, ",", self.y, ")")

    def set(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # Operações matemáticas entre pontos
    def __add__(self, other):
        return Ponto(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Ponto(self.x - other.x, self.y - other.y)

    def __mul__(self, escalar: float):
        return Ponto(self.x * escalar, self.y * escalar)

# Classe que representa um quadrado
class Quadrado:
    def __init__(self, w, h):
        self.pos = Ponto(0, 0)    # Posição do quadrado
        self.w = w                # Largura
        self.h = h                # Altura
        self.c = (1, 0, 0)        # Cor (vermelho por padrão)
        self.r = 0                # Ângulo de rotação em graus

# Lista de quadrados e controle de qual está ativo
quadrados = [Quadrado(0.25, 0.25)]
num_quadrado = 0

# Controle de tempo para animação
tempo_antes = time.time()
soma_dt = 0

# Parâmetros da câmera (pan e viewport)
left = 0
right = 0
top = 0
bottom = 0
panX = 0
panY = 0

# Desenha os eixos X e Y no mundo
def desenhaEixos():
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)
    glLineWidth(1)

    glBegin(GL_LINES)
    glVertex2f(left, 0)
    glVertex2f(right, 0)
    glVertex2f(0, bottom)
    glVertex2f(0, top)
    glEnd()

    glPopMatrix()

# Desenha um quadrado na posição (x, y), com rotação r
def desenhaQuadrado(x, y, w, h, r):
    glPushMatrix()

    glTranslatef(x, y, 0)     # Move para a posição desejada
    glRotatef(r, 0, 0, 1)     # Rotaciona em torno do eixo Z (plano XY)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()

    glPopMatrix()

# Função principal de redesenho da cena
def Desenha():
    global left, right, top, bottom, panX, panY

    # Define projeção ortográfica com pan
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    # Limpa a tela
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # Desenha todos os quadrados
    for quadrado in quadrados:
        glColor3f(*quadrado.c)
        desenhaQuadrado(quadrado.pos.x, quadrado.pos.y, quadrado.h, quadrado.w, quadrado.r)

    # Desenha os eixos (ajuda visual)
    desenhaEixos()

    # Finaliza os comandos de renderização
    glFlush()

# Função chamada constantemente (idle) para atualizar a animação
def Animacao():
    global soma_dt, tempo_antes

    tempo_agora = time.time()
    delta_time = tempo_agora - tempo_antes
    tempo_antes = tempo_agora

    soma_dt += delta_time

    if soma_dt > 1.0 / 30:  # Aproximadamente 30 quadros por segundo
        soma_dt = 0

        # Atualiza o ângulo de rotação do quadrado atual
        # O % 360 garante que o valor fique entre 0 e 359 (rotação cíclica)
        quadrados[num_quadrado].r = (quadrados[num_quadrado].r + 1) % 360

        glutPostRedisplay()  # Solicita redesenho da tela

# Gerencia as teclas do teclado comum (ASCII)
def Teclado(key: chr, x: int, y: int):
    global num_quadrado, panX, panY

    if key == 27:  # ESC
        exit(0)

    if key == b' ':
        # Cria um novo quadrado e incrementa o índice
        quadrados.append(Quadrado(0.25, 0.25))
        num_quadrado += 1
        quadrados[num_quadrado].c = (
            num_quadrado / 9 % 3 / 2.0,
            num_quadrado / 3 % 3 / 2.0,
            num_quadrado % 3 / 2.0
        )

    # Controle da câmera (pan) com WASD
    if key == b'a':
        panX -= 0.01
    if key == b'd':
        panX += 0.01
    if key == b'w':
        panY += 0.01
    if key == b's':
        panY -= 0.01

    glutPostRedisplay()

# Gerencia teclas especiais (setas) para mover o quadrado ativo
def TeclasEspeciais(key: int, x: int, y: int):
    if key == GLUT_KEY_LEFT:
        quadrados[num_quadrado].pos -= Ponto(0.02, 0)
    if key == GLUT_KEY_RIGHT:
        quadrados[num_quadrado].pos += Ponto(0.02, 0)
    if key == GLUT_KEY_UP:
        quadrados[num_quadrado].pos += Ponto(0, 0.02)
    if key == GLUT_KEY_DOWN:
        quadrados[num_quadrado].pos -= Ponto(0, 0.02)

    glutPostRedisplay()

# Inicializa os parâmetros da câmera
def Inicializa():
    global left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 1
    top = 1
    bottom = -1
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

# Função principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Desenha OpenGL")

    glutDisplayFunc(Desenha)
    glutIdleFunc(Animacao)
    glutKeyboardFunc(Teclado)
    glutSpecialFunc(TeclasEspeciais)

    Inicializa()

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()
