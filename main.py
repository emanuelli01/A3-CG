import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from faces import draw_rubiks_cube, rotate_face

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                # Rotaciona nos eixos x, y e z
                if event.key == pygame.K_LEFT:
                    rotate_face('y', 0, 90)  
                elif event.key == pygame.K_RIGHT:
                    rotate_face('y', 2, -90)  
                elif event.key == pygame.K_UP:
                    rotate_face('x', 2, 90) 
                elif event.key == pygame.K_DOWN:
                    rotate_face('x', 0, -90)  
                elif event.key == pygame.K_z:
                    rotate_face('z', 0, 90) 
                elif event.key == pygame.K_x:
                    rotate_face('z', 2, -90) 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_rubiks_cube()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()