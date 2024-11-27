from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Matriz para rastrear o estado do cubo
# Cada cubo menor terá uma posição inicial e será representado por um índice.
# A matriz representa o Cubo Mágico no formato 3x3x3.
cube_state = np.array([[[x, y, z] for z in range(-1, 2)] for y in range(-1, 2) for x in range(-1, 2)])
cube_state = cube_state.reshape(3, 3, 3, 3)  # Estrutura 3D para organizar posições

# Função para desenhar um cubo pequeno (cada cubo pequeno será uma das 27 faces do cubo)
def draw_cube():
    """Desenha um cubo básico com cores em cada face."""
    vertices = [
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
    ]
    faces = [
        (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (3, 2, 6, 7), (1, 5, 6, 2), (0, 4, 7, 3)
    ]
    colors = [
        [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0.5, 0], [1, 1, 1]
    ]
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_rubiks_cube():
    """Desenha todos os 27 cubos menores."""
    spacing = 1.1  # Espaço entre cubos
    for x in range(3):  # Eixo X
        for y in range(3):  # Eixo Y
            for z in range(3):  # Eixo Z
                glPushMatrix()
                # move cada cubo pequeno para posição rastreada pela matriz
                position = cube_state[x][y][z]
                glTranslatef(position[0] * spacing, position[1] * spacing, position[2] * spacing)
                draw_cube()
                glPopMatrix()

def rotate_face(axis, layer, angle):
    """
    Rotaciona uma camada específica ao longo de um eixo.
    - axis: 'x', 'y', ou 'z' (eixo da rotação)
    - layer: camada do cubo (0, 1 ou 2 no eixo)
    - angle: ângulo de rotação (em graus, pode ser positivo ou negativo)
    """
    # Seleciona os índices dos cubos na camada correta
    if axis == 'x':
        indices = cube_state[layer, :, :]
    elif axis == 'y':
        indices = cube_state[:, layer, :]
    elif axis == 'z':
        indices = cube_state[:, :, layer]
    else:
        raise ValueError("Eixo inválido. Escolha 'x', 'y' ou 'z'.")

    # Aplica a rotação nos índices da camada (no estado do cubo)
    rotation_matrix = None
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0], [0, np.cos(np.radians(angle)), -np.sin(np.radians(angle))], [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(np.radians(angle)), 0, np.sin(np.radians(angle))], [0, 1, 0], [-np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))]])
    elif axis == 'z':
        rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0], [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0], [0, 0, 1]])

    # Atualiza os estados de posição
    for pos in np.nditer(indices, op_flags=['readwrite']):
        pos[...] = np.dot(rotation_matrix, pos)

