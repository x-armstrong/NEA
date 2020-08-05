import sys, pygame #import pygame, the main library used for graphics

pygame.init() #initialise all of the pygame modules for later use

screen = pygame.display.set_mode([1200, 900]) #Create a window with the given dimensions
pygame.display.set_caption("Photoelectric Effect Simulator V-Alpha") #Set the title of the window

#Create the main "game loop"
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
