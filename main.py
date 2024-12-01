import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Constantes de cores
COLORS = {
    'WHITE': (1, 1, 1),
    'YELLOW': (1, 1, 0),
    'RED': (1, 0, 0),
    'ORANGE': (1, 0.5, 0),
    'BLUE': (0, 0, 1),
    'GREEN': (0, 1, 0),
    'BLACK': (0, 0, 0)  # Added BLACK color
}
EPSILON = 1e-5  # Ajuste conforme necessário



import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Constantes de cores
COLORS = {
    'WHITE': (1, 1, 1),
    'YELLOW': (1, 1, 0),
    'RED': (1, 0, 0),
    'ORANGE': (1, 0.5, 0),
    'BLUE': (0, 0, 1),
    'GREEN': (0, 1, 0),
    'BLACK': (0, 0, 0)  # Cor padrão para faces invisíveis
}
EPSILON = 1e-5


class Cubelet:
    def __init__(self, position):
        """
        Inicializa um cubelet (pequeno cubo) com cores padrão baseadas na posição
        """
        self.position = np.array(position, dtype=float)
        self.colors = self._get_default_colors(position)

    def _get_default_colors(self, pos):
        """
        Define as cores padrão com base na posição inicial do cubo
        """
        x, y, z = pos
        colors = [
            COLORS['GREEN'] if np.abs(z - 1) < EPSILON else COLORS['BLACK'],  # Frente
            COLORS['BLUE'] if np.abs(z + 1) < EPSILON else COLORS['BLACK'],  # Trás
            COLORS['ORANGE'] if np.abs(x + 1) < EPSILON else COLORS['BLACK'],  # Esquerda
            COLORS['RED'] if np.abs(x - 1) < EPSILON else COLORS['BLACK'],  # Direita
            COLORS['WHITE'] if np.abs(y - 1) < EPSILON else COLORS['BLACK'],  # Topo
            COLORS['YELLOW'] if np.abs(y + 1) < EPSILON else COLORS['BLACK']  # Base
        ]
        return colors

    def update_colors(self, axis, direction):
        """
        Atualiza as cores do cubelet após uma rotação.
        """
        if axis == 'x':
            if direction == 1:
                # Gira as cores no sentido horário no eixo X - A
                self.colors = [
                    self.colors[4],  # Topo -> Frente
                    self.colors[5],  # Base -> Trás
                    self.colors[2],  # Esquerda permanece
                    self.colors[3],  # Direita permanece
                    self.colors[1],  # Frente -> Base
                    self.colors[0]   # Trás -> Topo
                ]

        elif axis == 'y':
            if direction == 1:
                # Gira as cores no sentido horário no eixo Y
                self.colors = [
                    self.colors[2],  # Esquerda -> Frente
                    self.colors[3],  # Direita -> Trás
                    self.colors[1],  # Frente -> Direita
                    self.colors[0],  # Trás -> Esquerda
                    self.colors[4],  # Topo permanece
                    self.colors[5]   # Base permanece
                ]

        elif axis == 'z':
            if direction == 1:
                # Gira as cores no sentido horário no eixo Z - E
                self.colors = [
                    self.colors[0],  # Direita -> Frente
                    self.colors[1],  # Esquerda -> Trás
                    self.colors[4],  # Topo -> Direita
                    self.colors[5],  # Base -> Esquerda
                    self.colors[3],  # Frente -> Topo
                    self.colors[2]   # Trás -> Base
                ]


    def draw(self, half=0.4):
        """
        Desenha o cubelet usando OpenGL
        """
        x, y, z = self.position
        faces = [
            ([x - half, y - half, z + half], [x + half, y - half, z + half], [x + half, y + half, z + half],
             [x - half, y + half, z + half]),  # Frente
            ([x - half, y - half, z - half], [x + half, y - half, z - half], [x + half, y + half, z - half],
             [x - half, y + half, z - half]),  # Trás
            ([x - half, y - half, z - half], [x - half, y - half, z + half], [x - half, y + half, z + half],
             [x - half, y + half, z - half]),  # Esquerda
            ([x + half, y - half, z - half], [x + half, y - half, z + half], [x + half, y + half, z + half],
             [x + half, y + half, z - half]),  # Direita
            ([x - half, y + half, z - half], [x + half, y + half, z - half], [x + half, y + half, z + half],
             [x - half, y + half, z + half]),  # Topo
            ([x - half, y - half, z - half], [x + half, y - half, z - half], [x + half, y - half, z + half],
             [x - half, y - half, z + half]),  # Base
        ]

        for i, face in enumerate(faces):
            glColor3fv(self.colors[i])
            glBegin(GL_QUADS)
            for vertex in face:
                glVertex3fv(vertex)
            glEnd()


class RubiksCube:
    def __init__(self):
        """Inicializa o cubo mágico com todos os cubelets"""
        self.cubelets = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    self.cubelets.append(Cubelet([x, y, z]))

        # Estado de rotação
        self.rotating_layer = None
        self.rotation_progress = 0
        self.rotation_speed = 0.2
        self.rotation_axis = None
        self.rotation_direction = None
        self.rotation_layer_value = None

    def draw(self):
        """Desenha todos os cubelets do cubo"""
        for cubelet in self.cubelets:
            cubelet.draw()


    def rotate_layer(self, axis, layer_value, direction):
        """
        Inicia a rotação de uma camada específica
        axis: 'x', 'y' ou 'z'
        layer_value: valor da coordenada da camada a ser rotacionada
        direction: 1 (sentido horário) ou -1 (anti-horário)
        """
        if self.rotating_layer is None:
            axis_map = {'x': 0, 'y': 1, 'z': 2}
            self.rotating_layer = [
                cubelet for cubelet in self.cubelets
                if np.isclose(cubelet.position[axis_map[axis]], layer_value)
            ]
            self.rotation_axis = axis
            self.rotation_direction = direction
            self.rotation_layer_value = layer_value
            self.rotation_progress = 0

    def update_rotation(self):
        """Atualiza o estado de rotação da camada"""
        if self.rotating_layer is not None:
            self.rotation_progress += self.rotation_speed

            # Calcula o ângulo de rotação
            rotation_angle = np.pi / 2 * self.rotation_speed * self.rotation_direction

            # Cria matriz de rotação
            rotation_matrix = self._get_rotation_matrix(self.rotation_axis, rotation_angle)

            # Rotaciona cada cubelet da camada
            for cubelet in self.rotating_layer:
                cubelet.position = np.dot(rotation_matrix, cubelet.position)

            # Verifica se a rotação está completa
            if self.rotation_progress >= 1:
                # Finaliza a rotação
                self.rotation_progress = 0
                for cubelet in self.rotating_layer:
                    cubelet.position = np.where(np.isclose(cubelet.position, 0), 0,
                                                np.where(np.isclose(cubelet.position, 1), 1,
                                                         np.where(np.isclose(cubelet.position, -1), -1,
                                                                  cubelet.position)))

                    cubelet.update_colors(self.rotation_axis, self.rotation_direction)

                # Limpa o estado de rotação
                self.rotating_layer = None
                self.rotation_axis = None
                self.rotation_direction = None
                self.rotation_layer_value = None

    def _get_rotation_matrix(self, axis, angle):
        """Gera matriz de rotação para um eixo específico"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)

        if axis == 'x':
            return np.array([
                [1, 0, 0],
                [0, cos_a, -sin_a],
                [0, sin_a, cos_a]
            ])
        elif axis == 'y':
            return np.array([
                [cos_a, 0, sin_a],
                [0, 1, 0],
                [-sin_a, 0, cos_a]
            ])
        else:  # 'z'
            return np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ])


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cubo de Rubik Interativo")

    # Configuração da perspectiva
    gluPerspective(55, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    # Habilita profundidade
    glEnable(GL_DEPTH_TEST)

    rubiks_cube = RubiksCube()

    # Variáveis de rotação do cubo
    rotation_x, rotation_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Rotação de camadas
            if event.type == pygame.KEYDOWN:
                # Camada Y (vertical)
                if event.key == pygame.K_w:
                    rubiks_cube.rotate_layer('y', 1, 1)
                if event.key == pygame.K_s:
                    rubiks_cube.rotate_layer('y', -1, 1)

                # Camada X (horizontal)
                if event.key == pygame.K_a:
                    rubiks_cube.rotate_layer('x', -1, 1)
                if event.key == pygame.K_d:
                    rubiks_cube.rotate_layer('x', 1, 1)

                # Camada Z (profundidade)
                if event.key == pygame.K_q:
                    rubiks_cube.rotate_layer('z', -1, 1)
                if event.key == pygame.K_e:
                    rubiks_cube.rotate_layer('z', 1, 1)

        # Rotação do cubo inteiro com teclas de seta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rotation_y -= 3.5
        if keys[pygame.K_RIGHT]:
            rotation_y += 3.5
        if keys[pygame.K_UP]:
            rotation_x -= 3.5
        if keys[pygame.K_DOWN]:
            rotation_x += 3.5

        # Atualiza rotação da camada
        rubiks_cube.update_rotation()

        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Aplica rotação geral do cubo
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)

        # Desenha o cubo
        rubiks_cube.draw()

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
