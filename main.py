import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Definição das cores (RGB)
colors = {
    "white": [1.0, 1.0, 1.0],
    "yellow": [1.0, 1.0, 0.0],
    "red": [1.0, 0.0, 0.0],
    "orange": [1.0, 0.5, 0.0],
    "blue": [0.0, 0.0, 1.0],
    "green": [0.0, 1.0, 0.0]
}

# Representação das faces do cubo como matrizes 3x3
cube_faces = {
    "front": np.array([["green"]*3]*3),
    "back": np.array([["blue"]*3]*3),
    "top": np.array([["white"]*3]*3),
    "bottom": np.array([["yellow"]*3]*3),
    "left": np.array([["orange"]*3]*3),
    "right": np.array([["red"]*3]*3),
}

def draw_face(color, offset_x, offset_y, offset_z, normal):
    size = 0.33  # Tamanho de cada quadrado
    padding = 0.01  # Espaço entre os quadrados

    glBegin(GL_QUADS)
    for i in range(3):
        for j in range(3):
            glColor3fv(color)  # Define a cor do quadrado
            x = offset_x + (i * (size + padding))
            y = offset_y + (j * (size + padding))
            z = offset_z

            if normal == 'x':
                glVertex3f(z, x, y)
                glVertex3f(z, x + size, y)
                glVertex3f(z, x + size, y + size)
                glVertex3f(z, x, y + size)
            elif normal == 'y':
                glVertex3f(x, z, y)
                glVertex3f(x + size, z, y)
                glVertex3f(x + size, z, y + size)
                glVertex3f(x, z, y + size)
            elif normal == 'z':
                glVertex3f(x, y, z)
                glVertex3f(x + size, y, z)
                glVertex3f(x + size, y + size, z)
                glVertex3f(x, y + size, z)
    glEnd()

def draw_cube():
    """Desenha o cubo mágico completo com faces 3x3"""
    # Frente (verde)
    draw_face(colors["green"], -0.5, -0.5, 0.5, 'z')  # Cor verde para a frente

    # Trás (azul)
    draw_face(colors["blue"], -0.5, -0.5, -0.5, 'z')  # Cor azul para a parte de trás

    # Superior (branca)
    draw_face(colors["white"], -0.5, -0.5, 0.5, 'y')  # Cor branca para a parte superior

    # Inferior (amarela)
    draw_face(colors["yellow"], -0.5, -0.5, -0.5, 'y')  # Cor amarela para a parte inferior

    # Direita (vermelha)
    draw_face(colors["red"], -0.5, -0.5, -0.5, 'x')  # Cor vermelha para a parte direita (ajustado)

    # Esquerda (laranja)
    draw_face(colors["orange"], -0.5, -0.5, 0.5, 'x')  # Cor laranja para a parte esquerda

def rotate_layer(layer, direction='clockwise'):
    """Função para girar uma camada"""
    if direction == 'clockwise':
        return np.rot90(layer, -1)  # Rotaciona para a direita
    else:
        return np.rot90(layer, 1)  # Rotaciona para a esquerda

def rotate_top_layer(direction='clockwise'):
    """Função para girar a camada superior"""
    cube_faces["top"] = rotate_layer(cube_faces["top"], direction)
    cube_faces["front"][0], cube_faces["left"][0], cube_faces["back"][0], cube_faces["right"][0] = \
        cube_faces["left"][0], cube_faces["back"][0], cube_faces["right"][0], cube_faces["front"][0]

def rotate_bottom_layer(direction='clockwise'):
    """Função para girar a camada inferior"""
    cube_faces["bottom"] = rotate_layer(cube_faces["bottom"], direction)
    cube_faces["front"][2], cube_faces["left"][2], cube_faces["back"][2], cube_faces["right"][2] = \
        cube_faces["right"][2], cube_faces["front"][2], cube_faces["left"][2], cube_faces["back"][2]

def rotate_left_layer(direction='clockwise'):
    """Função para girar a camada esquerda"""
    cube_faces["left"] = rotate_layer(cube_faces["left"], direction)
    cube_faces["front"][:, 0], cube_faces["top"][:, 0], cube_faces["bottom"][:, 0], cube_faces["back"][:, 2] = \
        cube_faces["top"][:, 0], cube_faces["back"][:, 2], cube_faces["bottom"][:, 0], cube_faces["front"][:, 0]

def rotate_right_layer(direction='clockwise'):
    """Função para girar a camada direita"""
    cube_faces["right"] = rotate_layer(cube_faces["right"], direction)
    cube_faces["front"][:, 2], cube_faces["top"][:, 2], cube_faces["bottom"][:, 2], cube_faces["back"][:, 0] = \
        cube_faces["back"][:, 0], cube_faces["top"][:, 2], cube_faces["front"][:, 2], cube_faces["bottom"][:, 2]

def rotate_front_layer(direction='clockwise'):
    """Função para girar a camada frontal"""
    cube_faces["front"] = rotate_layer(cube_faces["front"], direction)
    cube_faces["top"][2], cube_faces["left"][:, 2], cube_faces["bottom"][0], cube_faces["right"][:, 0] = \
        cube_faces["left"][:, 2], cube_faces["bottom"][0], cube_faces["right"][:, 0], cube_faces["top"][2]

def rotate_back_layer(direction='clockwise'):
    """Função para girar a camada traseira"""
    cube_faces["back"] = rotate_layer(cube_faces["back"], direction)
    cube_faces["top"][0], cube_faces["right"][:, 2], cube_faces["bottom"][2], cube_faces["left"][:, 0] = \
        cube_faces["right"][:, 2], cube_faces["bottom"][2], cube_faces["left"][:, 0], cube_faces["top"][0]

def main():
    """Função principal para criar a janela, configurar o OpenGL e gerenciar eventos."""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Configuração de perspectiva
    glTranslatef(0.0, 0.0, -5)  # Posiciona a câmera

    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade para garantir que as faces não fiquem invisíveis

    rotation_x, rotation_y = 0, 0  # Ângulos de rotação

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotation_y -= 15  # Rotaciona à esquerda
                if event.key == pygame.K_RIGHT:
                    rotation_y += 15  # Rotaciona à direita
                if event.key == pygame.K_UP:
                    rotation_x -= 15  # Rotaciona para cima
                if event.key == pygame.K_DOWN:
                    rotation_x += 15  # Rotaciona para baixo

                # Teclas para girar as camadas
                if event.key == pygame.K_w:
                    rotate_top_layer('clockwise')
                if event.key == pygame.K_s:
                    rotate_bottom_layer('clockwise')
                if event.key == pygame.K_a:
                    rotate_left_layer('clockwise')
                if event.key == pygame.K_d:
                    rotate_right_layer('clockwise')
                if event.key == pygame.K_e:
                    rotate_front_layer('clockwise')
                if event.key == pygame.K_q:
                    rotate_back_layer('clockwise')

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Aplica as rotações da câmera
        glRotatef(rotation_x, 1, 0, 0)  # Rotação no eixo X
        glRotatef(rotation_y, 0, 1, 0)  # Rotação no eixo Y

        draw_cube()  # Desenha o cubo mágico

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
