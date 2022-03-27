import os.path
from unittest import result
import time
import pygame
from Autopoiesis import AutopoiesisRecord
from Environment import Environment
import numpy as np

Duration = 2000
Recorder = [AutopoiesisRecord(Duration) for _ in range(8)]

def rgba2rgb( rgba, background=(255,255,255) ):
    a=rgba[3]
    R, G, B = background
    rgba[0] = min(rgba[0] * a + (1.0 - a) * R,255)
    rgba[1] = min(rgba[1] * a + (1.0 - a) * G,255)
    rgba[2] = min(rgba[2] * a + (1.0 - a) * B,255)
    return rgba[0:3]

def sysInit(E,StartTime,Duration):
    pygame.init()
    box = 30
    padding = 2
    screen = pygame.display.set_mode((1900, 1900))
    pygame.display.set_caption("ASystem")
    screen.fill((255, 255, 255))
    fcclock = pygame.time.Clock()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont("Times New Roman", 50)
    barfont = pygame.font.SysFont("Times New Roman", 40)
    indexfont = pygame.font.SysFont("Times New Roman", 40)
    running = True

    Time=0
    while Time<Duration and running:
        Time +=1
        screen.fill("white")
        c=E.Plot("Phospholipids")
        # Draw Color Bar
        for j in range(255):
            pygame.draw.rect(screen, rgba2rgb([0, 255, 0, (255-j) / 255]), (len(c)*32+150, j * 3+150, 100, 20), 0)
        for i in range(6):
            textsurface = barfont.render('%.1f' % (1-i/5), False, (0, 0, 0))
            screen.blit(textsurface, ((len(c)*32+80, 150+i*150, 100, 20)))
        ####
        for i in range(len(c)):
            for j in range(len(c[0])):
                pygame.draw.rect(screen, rgba2rgb([0, 255, 0,min(c[i][j],0.8)]), (i * (box + padding)+30,
                                                             j * (box + padding)+30,
                                                             box,
                                                             box), 0)
        for index in range(len(E.AutopoiesisList)):
            pygame.draw.rect(screen,rgba2rgb([255,0,0,1]),(E.AutopoiesisList[index].coorx * (box + padding)-box//3+30,
                                                             E.AutopoiesisList[index].coory * (box + padding)+30,
                                                             box,
                                                             box))
            textsurface = indexfont.render(str(E.AutopoiesisList[index].id),False, (0, 0, 0))

            Recorder[E.AutopoiesisList[index].id].Integrity[Time]=E.AutopoiesisList[index].Integrity(E.Blocks)
            Recorder[E.AutopoiesisList[index].id].size[Time]=E.AutopoiesisList[index].radius
            Recorder[E.AutopoiesisList[index].id].locationx[Time]=E.AutopoiesisList[index].coorx
            Recorder[E.AutopoiesisList[index].id].locationy[Time]=E.AutopoiesisList[index].coory
            screen.blit(textsurface, (E.AutopoiesisList[index].coorx*(box+padding), E.AutopoiesisList[index].coory*(box+padding)))
            textsurface = myfont.render('Autopoiesis %d\'s Integrity: %.4f' % (E.AutopoiesisList[index].id,E.AutopoiesisList[index].Integrity(E.Blocks)) , False, (0, 0, 0))
            screen.blit(textsurface, (100, 1650+index*60))
            textsurface = myfont.render(
                'Autopoiesis %d\'s Perimeter: %d' % (E.AutopoiesisList[index].id, E.AutopoiesisList[index].Perimeter), False, (0, 0, 0))
            screen.blit(textsurface, (800, 1650 + index * 60))
        textsurface = myfont.render('Time=%d' % Time, False,(0, 0, 0))
        screen.blit(textsurface, (100, 100))
        E.Update()
        fcclock.tick(60)
        pygame.display.update()
        if Time%25==0 or Time<25:
            pygame.image.save(screen, StartTime+"/screenshot%d.jpeg"%Time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




if __name__ == "__main__":
    #autopoiesis=[(15,15,4),(35,35,4),(15,35,4),(35,15,4)]
    ionsLimit={"Phospholipids": 0.15,"amino acid":0.01}

    sizex=50
    sizey=sizex

    autopoiesis=[(sizex//2,sizey//2,3)]
    E = Environment(ionsLimit,sizex,sizey,autopoiesis,True)
    StartTime = time.strftime("%m-%d-%H-%M-%S", time.localtime())
    os.mkdir(StartTime+"/")
    sysInit(E,StartTime,Duration)


