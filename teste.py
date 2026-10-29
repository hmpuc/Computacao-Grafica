"""
Controles:
    1 a 9/0 ........ selecionam os exercícios 1 a 10
    setas ou N/P . seleciona o próximo/anterior
    ESC .......... fecha o programa
"""

import os
import sys

# Em alguns sistemas Linux, pode ser necessário comentar este bloco ou
# trocar "glx" pelo backend OpenGL disponível na máquina.
if sys.platform.startswith("linux"):
    os.environ.setdefault("PYOPENGL_PLATFORM", "glx")

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


exercicio_atual = 1

# Uma cor para cada número de segmento.
CORES = {
    1: (0.05, 0.45, 0.85),  # azul
    2: (0.90, 0.25, 0.05),  # laranja
    3: (0.55, 0.15, 0.70),  # roxo
    4: (0.05, 0.65, 0.25),  # verde
}

def escreve_texto(x, y, texto, fonte=GLUT_BITMAP_HELVETICA_18):
    """Escreve texto na posição corrente do sistema de coordenadas."""
    glRasterPos2f(x, y)
    for caractere in texto:
        glutBitmapCharacter(fonte, ord(caractere))


def desenha_segmento(numero, tracejado=False, posicao_num=(0.8, 5.0)):
    """Representa o código do método Desenha()"""
    glColor3f(*CORES[numero])
    glLineWidth(5.0)

    if tracejado: # em caso de overlap
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(2, 0x00FF)

    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(0, 10)
    glEnd()

    if tracejado:
        glDisable(GL_LINE_STIPPLE)

    escreve_texto(posicao_num[0], posicao_num[1], str(numero))


def desenha_grade_e_eixos():
    """Desenha uma ggrid."""
    glPushMatrix()
    glLoadIdentity()

    # Passos de 10 em 10
    glLineWidth(1.0)
    glColor3f(0.80, 0.80, 0.80)
    glBegin(GL_LINES)
    for valor in range(-30, 61, 10):
        glVertex2f(valor, -30)
        glVertex2f(valor, 50)
    for valor in range(-30, 51, 10):
        glVertex2f(-30, valor)
        glVertex2f(60, valor)
    glEnd()

    #Eixos
    glColor3f(0.25, 0.25, 0.25)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(-30, 0)
    glVertex2f(60, 0)
    glVertex2f(0, -30)
    glVertex2f(0, 50)
    glEnd()

    glPopMatrix()


def exercicio_1():
    glTranslatef(10, 0, 0)
    desenha_segmento(1)

    glTranslatef(10, 0, 0)
    desenha_segmento(2)

    glTranslatef(0, 10, 0)
    desenha_segmento(3)

    glTranslatef(-20, 0, 0)
    desenha_segmento(4)


def exercicio_2():
    glTranslatef(10, 0, 0)
    desenha_segmento(1)

    glTranslatef(10, 0, 0)
    desenha_segmento(2)

    glLoadIdentity()

    glTranslatef(0, 10, 0)
    desenha_segmento(3)

    glTranslatef(10, 0, 0)
    desenha_segmento(4)


def exercicio_3():
    desenha_segmento(1)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(2)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(3)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(4)


def exercicio_4():
    glTranslatef(10, 10, 0)
    desenha_segmento(1)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(2)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(3)

    glRotatef(90, 0, 0, 1)
    desenha_segmento(4)


def exercicio_5():
    glTranslatef(20, 0, 0)
    glRotatef(90, 0, 0, 1)
    desenha_segmento(1)

    glLoadIdentity()

    glRotatef(90, 0, 0, 1)
    glTranslatef(20, 0, 0)
    desenha_segmento(2)


def exercicio_6():
    desenha_segmento(1)

    glTranslatef(10, 0, 0)
    glScalef(1, 2, 1)
    desenha_segmento(2)

    glTranslatef(10, 0, 0)
    glScalef(1, 0.5, 1)
    desenha_segmento(3)


def exercicio_7():
    glTranslatef(10, 0, 0)
    desenha_segmento(1, posicao_num=(1.2, 3.0))

    glPushMatrix()

    glTranslatef(10, 10, 0)
    glRotatef(90, 0, 0, 1)
    desenha_segmento(2)

    glPopMatrix()

    # Tracejado pq é igual ao 1
    desenha_segmento(3, tracejado=True, posicao_num=(-2.0, 7.0))


def exercicio_8():
    glPushMatrix()
    glTranslatef(10, 0, 0)
    desenha_segmento(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(20, 0, 0)
    glRotatef(90, 0, 0, 1)
    desenha_segmento(2)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(30, 0, 0)
    glRotatef(-90, 0, 0, 1)
    desenha_segmento(3)
    glPopMatrix()

    desenha_segmento(4)


def exercicio_9():
    glTranslatef(20, 10, 0)
    desenha_segmento(1)

    glPushMatrix()

    glRotatef(90, 0, 0, 1)
    desenha_segmento(2)

    glTranslatef(10, 0, 0)
    desenha_segmento(3)

    glPopMatrix()

    glTranslatef(10, 0, 0)
    desenha_segmento(4)


def exercicio_10():
    glTranslatef(10, 0, 0)

    glPushMatrix()

    glRotatef(90, 0, 0, 1)
    desenha_segmento(1, posicao_num=(0.8, 3.0))

    glPushMatrix()

    glTranslatef(10, 0, 0)
    glScalef(1, 2, 1)
    desenha_segmento(2)

    glPopMatrix()

    # Tracejado pq é igual ao 1
    desenha_segmento(3, tracejado=True, posicao_num=(-1.8, 7.0))

    glPopMatrix()

    desenha_segmento(4)


EXERCICIOS = {
    1: exercicio_1,
    2: exercicio_2,
    3: exercicio_3,
    4: exercicio_4,
    5: exercicio_5,
    6: exercicio_6,
    7: exercicio_7,
    8: exercicio_8,
    9: exercicio_9,
    10: exercicio_10,
}


def desenha_interface():
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.08, 0.12, 0.18)
    escreve_texto(-23, 37, f"Exercicio {exercicio_atual}")

    # Cor escura sobre fundo branco: agora esta linha fica visível.
    glColor3f(0.15, 0.18, 0.22)
    escreve_texto(
        -23,
        -18,
        "Teclas 1 até 0, setas ou N/P para selecionar um exercício | ESC: sair",
        GLUT_BITMAP_HELVETICA_12,
    )

    glPopMatrix()


def desenha():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    desenha_grade_e_eixos()

    # Carrega a identidade para cada exercício
    glLoadIdentity()
    EXERCICIOS[exercicio_atual]()

    desenha_interface()
    glutSwapBuffers()


def seleciona_exercicio(numero):
    global exercicio_atual
    exercicio_atual = ((numero - 1) % 10) + 1
    print(f"Exercicio {exercicio_atual}")
    glutPostRedisplay()


def teclado(tecla, x, y):
    if tecla == b"\x1b":
        os._exit(0)

    if tecla in b"123456789":
        seleciona_exercicio(int(tecla.decode("ascii")))
    elif tecla == b"0":
        seleciona_exercicio(10)
    elif tecla.lower() == b"n":
        seleciona_exercicio(exercicio_atual + 1)
    elif tecla.lower() == b"p":
        seleciona_exercicio(exercicio_atual - 1)


def teclas_especiais(tecla, x, y):
    if tecla in (GLUT_KEY_RIGHT, GLUT_KEY_UP):
        seleciona_exercicio(exercicio_atual + 1)
    elif tecla in (GLUT_KEY_LEFT, GLUT_KEY_DOWN):
        seleciona_exercicio(exercicio_atual - 1)


def inicializa():
    glClearColor(1, 1, 1, 1)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-25, 55, -20, 40)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(900, 700)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Exercicio de Transformacoes com OpenGL")

    glutDisplayFunc(desenha)
    glutKeyboardFunc(teclado)
    glutSpecialFunc(teclas_especiais)

    inicializa()
    seleciona_exercicio(1)

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == "__main__":
    main()