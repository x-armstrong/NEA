import sys, pygame #import pygame, the main library used for graphics
import random

mainClock = pygame.time.Clock()

pygame.init() #initialise all of the pygame modules for later use

#Variables for window size
screen_width = 1200
screen_height = 900

white = (255, 255, 255)
black = (0, 0, 0)
screen_background = (145, 194, 255)

screen = pygame.display.set_mode([screen_width, screen_height]) #Creates the screen itself
screen.fill(screen_background) #Set the background color of the window
pygame.display.set_caption("Photoelectric Effect Simulator V-Alpha") #Set the title of the window

def close():
    pygame.quit()
    sys.exit()

class Button():
    def __init__(self, text, size, font, text_color, color_static, color_hover, button_pos, action):
        self.text = font.render(text, False, text_color)
        self.color_static = color_static
        self.color_hover = color_hover
        self.bg = color_static
        self.button_pos = button_pos #(x,y)
        self.size = size #(width, height)

        self.rect = pygame.draw.rect(screen, self.bg, (self.button_pos[0], self.button_pos[1], self.size[0], self.size[1]))
        self.call_action = action

    def draw(self):
        self.hover_mouse()
        self.rect = pygame.draw.rect(screen, self.bg, (self.button_pos[0], self.button_pos[1], self.size[0], self.size[1]))
        screen.blit(self.text, (self.rect.center[0] - self.text.get_width()/2, self.rect.center[1] - self.text.get_height()/2))

    def hover_mouse(self):
        self.bg = self.color_static
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = self.color_hover

            if pygame.mouse.get_pressed()[0] == 1:
                self.call_action()

#Create a function that will handle the main menu
def main_menu():

    titlefont = pygame.font.SysFont("consolas", 55) #Create a font for the visual title
    buttonfont = pygame.font.SysFont("consolas", 45) #Create a font for the text on the buttons

    title = titlefont.render("The Photoelectric Effect Simulator", True, white) #Set the text of the title, and give the colour white
    #Create the text for the buttons, and color them black

    #Some variables for the buttons, so if I decide to change anything later it will be easy to do
    button_width = 250
    button_height = 100
    hover_color = (170, 255, 236)

    start_button =  Button("Start", (button_width, button_height), buttonfont, black, white, hover_color, ((screen_width/6) - button_width/2, 650), main_simulation)
    quiz_button = Button("Quiz", (button_width, button_height), buttonfont, black, white, hover_color, ((screen_width/2) - button_width/2, 650), quiz)
    exit_button = Button("Exit", (button_width, button_height), buttonfont, black, white, hover_color, (5*(screen_width/6) - button_width/2, 650), close)

    buttons = [start_button, quiz_button, exit_button]

    #Waiting for a button to be pressed
    while True:

        #Blit the text objects to the screen in the necessary positions
        screen.blit(title, ((screen_width/2)-(title.get_width()/2), screen_height/5))
        for button in buttons:
            button.draw()


        #Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
        pygame.display.update()
        mainClock.tick(60) #The framerate is set to 60 fps; will help when managing the animation later

class Photon:
    def __init__(self, wavelength, end_pos):
        self.wavelength = wavelength
        self.end_pos = end_pos

    def draw(self, start_pos, i):
        reached_end = False
        steps = 120

        if i < steps+1:
            pygame.draw.circle(screen, white, (int(start_pos[0] + ((self.end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((self.end_pos[1]-start_pos[1])/steps)*i)), 10)
            ##print((int(start_pos[0] + ((self.end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((self.end_pos[1]-start_pos[1])/steps)*i)))
            i += 1

        return i

class PhotoElectron:
    def __init__(self, kinetic_energy):
        self.kinetic_energy = kinetic_energy

photon_1 = Photon(20, (random.randrange(35, 75), random.randrange(625, 865)))
photon_2 = Photon(30, (random.randrange(35, 75), random.randrange(625, 865)))

#Function to call the main simulation screen
def main_simulation():
    screen.fill(screen_background) #Remove all of the previous text and buttons
    pygame.display.set_caption("Photoelectric Effect Simulator - Simulation") #Update the window title

    running_sim = True
    metal_color = (255,255,255) #determined by database later
    i = 1
    i2 = 1

    while running_sim:

        #Temporary testing values to move a circle from a to b
        start_pos = (400, 550)

        screen.fill(screen_background) #Clear the screen again so the circle's previous position is removed

        metal_plate = pygame.draw.rect(screen, metal_color, (30, 620, 50, 250))
        pygame.draw.line(screen, (0,0,0), (80, 620), (400, 550))
        pygame.draw.line(screen, (0,0,0), (80, 745), (400, 550))
        pygame.draw.line(screen, (0,0,0), (80, 870), (400, 550))
        lamp = pygame.draw.circle(screen, (255,255,255), (400, 550), 15)

        #Drawing the photons
        i = photon_1.draw(start_pos, i)
        i2 = photon_2.draw(start_pos, i2)

        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            #If the user presses escape, return them to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_sim = False
                    screen.fill(screen_background)
                    pygame.display.set_caption("Photoelectric Effect Simulator - Menu")

        pygame.display.update()
        mainClock.tick(60)

#Function to call the quiz screen
def quiz():
    screen.fill(screen_background)
    pygame.display.set_caption("Photoelectric Effect Simulator - Quiz (W.I.P)")

    running_quiz = True

    while running_quiz:

        #Quiz stuff here

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_quiz = False
                    screen.fill(screen_background)
                    pygame.display.set_caption("Photoelectric Effect Simulator - Menu")

        pygame.display.update()
        mainClock.tick(60)


main_menu()
