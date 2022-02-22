import pygame
from Environment import Environment

def rgba2rgb( rgba, background=(255,255,255) ):
    a=rgba[3]
    R, G, B = background
    rgba[0] = min(rgba[0] * a + (1.0 - a) * R,255)
    rgba[1] = min(rgba[1] * a + (1.0 - a) * G,255)
    rgba[2] = min(rgba[2] * a + (1.0 - a) * B,255)
    return rgba[0:3]

def sysInit(E):
    pygame.init()
    box = 30
    padding = 2
    screen = pygame.display.set_mode((2400, 2400))
    pygame.display.set_caption("Autopoiesis")
    screen.fill((255, 255, 255))
    fcclock = pygame.time.Clock()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont("Ubuntu", 60)
    indexfont = pygame.font.SysFont("Ubuntu", 30)
    running = True
    while running:
        screen.fill("white")
        c=E.Plot("Phospholipids")
        for i in range(len(c)):
            for j in range(len(c[0])):
                pygame.draw.rect(screen, rgba2rgb([0, 255, 0,min(c[i][j],0.8)]), (i * (box + padding),
                                                             j * (box + padding),
                                                             box,
                                                             box), 0)
        for index in range(len(E.AutopoiesisList)):
            pygame.draw.rect(screen,rgba2rgb([255,0,0,1]),(E.AutopoiesisList[index].coorx * (box + padding)-box//3,
                                                             E.AutopoiesisList[index].coory * (box + padding),
                                                             box,
                                                             box))
            textsurface = indexfont.render(str(index),False, (0, 0, 0))
            screen.blit(textsurface, (E.AutopoiesisList[index].coorx*(box+padding), E.AutopoiesisList[index].coory*(box+padding)))
            textsurface = myfont.render('Autopoiesis %d\'s Integrity: %.4f' % (index,E.AutopoiesisList[index].Integrity(E.Blocks)) , False, (0, 0, 0))
            screen.blit(textsurface, (0, 1600+index*60))
        E.Update()
        fcclock.tick(10)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

autopoiesis=[(15,15,4),(35,35,4),(15,35,4),(35,15,4)]

E = Environment(50,50,autopoiesis)
sysInit(E)


