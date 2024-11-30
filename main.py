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
    "green": [0.0, 1.0, 0.0],
    "black": [0.0, 0.0, 0.0],  # Cor para as faces internas (invisíveis)
}

class SmallCube:
    """Representa um cubo pequeno do Rubik's Cube."""
    def __init__(self, position, face_colors):
        self.position = np.array(position)  # Posição central do cubo
        self.face_colors = face_colors  # Cores das faces

    def draw(self):
        """Desenha o cubo pequeno com suas faces coloridas."""
        x, y, z = self.position
        size = 0.3  # Tamanho do cubo

        faces = [
            ([x, y, z + size], [x + size, y, z + size], [x + size, y + size, z + size], [x, y + size, z + size]),  # Frente
            ([x, y, z], [x + size, y, z], [x + size, y + size, z], [x, y + size, z]),  # Trás
            ([x, y, z], [x, y + size, z], [x, y + size, z + size], [x, y, z + size]),  # Esquerda
            ([x + size, y, z], [x + size, y + size, z], [x + size, y + size, z + size], [x + size, y, z + size]),  # Direita
            ([x, y + size, z], [x + size, y + size, z], [x + size, y + size, z + size], [x, y + size, z + size]),  # Topo
            ([x, y, z], [x + size, y, z], [x + size, y, z + size], [x, y, z + size]),  # Base
        ]

        for i, face in enumerate(faces):
            glBegin(GL_QUADS)
            glColor3fv(self.face_colors[i])
            for vertex in face:
                glVertex3fv(vertex)
            glEnd()

class RubiksCube:
    """Representa o cubo mágico como um conjunto de cubos pequenos."""
    def __init__(self):
        self.cubes = []
        offset = 0.35  # Distância entre os centros dos cubos pequenos
        face_mapping = [
            colors["green"], colors["blue"],  # Frente, Trás
            colors["orange"], colors["red"],  # Esquerda, Direita
            colors["white"], colors["yellow"],  # Topo, Base
        ]

        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == 0 and y == 0 and z == 0:  # Ignorar o cubo central
                        continue

                    face_colors = [
                        face_mapping[0] if z == 1 else colors["black"],  # Frente
                        face_mapping[1] if z == -1 else colors["black"],  # Trás
                        face_mapping[2] if x == -1 else colors["black"],  # Esquerda
                        face_mapping[3] if x == 1 else colors["black"],  # Direita
                        face_mapping[4] if y == 1 else colors["black"],  # Topo
                        face_mapping[5] if y == -1 else colors["black"],  # Base
                    ]

                    self.cubes.append(SmallCube((x * offset, y * offset, z * offset), face_colors))

    def draw(self):
        """Desenha o cubo mágico completo."""
        for cube in self.cubes:
            cube.draw()

    def rotate_layer(self, axis, layer_value, direction):
        """Rotaciona uma camada específica do cubo mágico e atualiza as cores."""
        angle = np.radians(90) * direction
        rotation_matrix = self._get_rotation_matrix(axis, angle)

        # Filtrar cubos que estão na camada a ser rotacionada
        affected_cubes = [cube for cube in self.cubes if np.isclose(cube.position[axis_map[axis]], layer_value)]

        # Atualizar posições e cores dos cubos afetados
        for cube in affected_cubes:
            cube.position = np.dot(rotation_matrix, cube.position)
            self._rotate_colors(cube, axis, direction)

    def _rotate_colors(self, cube, axis, direction):
        """Atualiza as cores das faces do cubo pequeno após a rotação."""
        if axis == 'x':  # Eixo X
            if direction == 1:
                cube.face_colors[4], cube.face_colors[1], cube.face_colors[5], cube.face_colors[0] = \
                    cube.face_colors[1], cube.face_colors[5], cube.face_colors[0], cube.face_colors[4]
            else:
                cube.face_colors[4], cube.face_colors[0], cube.face_colors[5], cube.face_colors[1] = \
                    cube.face_colors[0], cube.face_colors[5], cube.face_colors[1], cube.face_colors[4]

        elif axis == 'y':  # Eixo Y
            if direction == 1:
                cube.face_colors[0], cube.face_colors[3], cube.face_colors[1], cube.face_colors[2] = \
                    cube.face_colors[2], cube.face_colors[0], cube.face_colors[3], cube.face_colors[1]
            else:
                cube.face_colors[0], cube.face_colors[2], cube.face_colors[1], cube.face_colors[3] = \
                    cube.face_colors[3], cube.face_colors[1], cube.face_colors[2], cube.face_colors[0]

        elif axis == 'z':  # Eixo Z
            if direction == 1:
                cube.face_colors[4], cube.face_colors[2], cube.face_colors[5], cube.face_colors[3] = \
                    cube.face_colors[3], cube.face_colors[4], cube.face_colors[2], cube.face_colors[5]
            else:
                cube.face_colors[4], cube.face_colors[3], cube.face_colors[5], cube.face_colors[2] = \
                    cube.face_colors[2], cube.face_colors[5], cube.face_colors[3], cube.face_colors[4]

    def _get_rotation_matrix(self, axis, angle):
        """Retorna a matriz de rotação para o eixo dado e ângulo."""
        if axis == 'x':
            return np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)],
            ])
        elif axis == 'y':
            return np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)],
            ])
        elif axis == 'z':
            return np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ])

axis_map = {'x': 0, 'y': 1, 'z': 2}

def main():
    """Função principal para criar a janela, configurar o OpenGL e gerenciar eventos."""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    glEnable(GL_DEPTH_TEST)

    rubiks_cube = RubiksCube()
    rotation_x, rotation_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controle de movimento das camadas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rubiks_cube.rotate_layer('y', 0.35, 1)
                if event.key == pygame.K_s:
                    rubiks_cube.rotate_layer('y', -0.35, 1)
                if event.key == pygame.K_a:
                    rubiks_cube.rotate_layer('x', -0.35, 1)
                if event.key == pygame.K_d:
                    rubiks_cube.rotate_layer('x', 0.35, 1)
                if event.key == pygame.K_e:
                    rubiks_cube.rotate_layer('z', 0.35, 1)
                if event.key == pygame.K_q:
                    rubiks_cube.rotate_layer('z', -0.35, 1)

        # Controle contínuo de rotação com as setas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rotation_y -= 3
        if keys[pygame.K_RIGHT]:
            rotation_y += 3
        if keys[pygame.K_UP]:
            rotation_x -= 3
        if keys[pygame.K_DOWN]:
            rotation_x += 3

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)

        rubiks_cube.draw()

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
