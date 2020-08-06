import sys, pygame #import pygame, the main library used for graphics

mainClock = pygame.time.Clock()

pygame.init() #initialise all of the pygame modules for later use

#Variables for window size
screen_width = 1200
screen_height = 900

white = (255, 255, 255)
screen_background = (145, 194, 255)

screen = pygame.display.set_mode([screen_width, screen_height]) #Creates the screen itself
screen.fill(screen_background) #Set the background color of the window
pygame.display.set_caption("Photoelectric Effect Simulator V-Alpha") #Set the title of the window

class Photon:
    def __init__(self,wavelength, start_pos, end_pos):
        self.wavelength = wavelength
        self.start_pos = start_pos
        self.end_pos = end_pos

test_photon = Photon(20, (200, 200), (600, 600))

def button_clicked(button, width, height, mouse, click):
    #Defines the bounds of the button
    if (button.topleft[0] < mouse[0] < button.topleft[0] + width) and (button.topleft[1] < mouse[1] < button.topleft[1] + height):

        #Draws a new rect of different colour to give the appearance of interaction.
        ##Consider different method; this covers the text
        pygame.draw.rect(screen, (170, 255, 236), button)

        #Button is pressed so return true
        if click[0] == 1:
            return True

#Create a function that will handle the main menu
def main_menu():

    titlefont = pygame.font.SysFont("consolas", 55) #Create a font for the visual title
    buttonfont = pygame.font.SysFont("consolas", 45) #Create a font for the text on the buttons

    title = titlefont.render("The Photoelectric Effect Simulator", True, white) #Set the text of the title, and give the colour white
    #Create the text for the buttons, and color them black
    start_text = buttonfont.render("Start", True, (0,0,0))
    quiz_text = buttonfont.render("Quiz", True, (0,0,0))
    exit_text = buttonfont.render("Exit", True, (0,0,0))

    #Some variables for the buttons, so if I decide to change anything later it will be easy to do
    button_width = 250
    button_height = 100
    button_color = white

    #Waiting for a button to be pressed
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #Draw the rect objects themselves on the screen, with necessary properties
        start_button = pygame.draw.rect(screen, button_color, ((screen_width/6) - button_width/2, 650, button_width, button_height)) #Start Simulation
        quiz_button = pygame.draw.rect(screen, button_color, ((screen_width/2) - button_width/2, 650, button_width, button_height)) #Quiz
        exit_button = pygame.draw.rect(screen, button_color, (5*(screen_width/6) - button_width/2, 650, button_width, button_height)) #Exit

        #Blit the text objects to the screen in the necessary positions
        screen.blit(title, ((screen_width/2)-(title.get_width()/2), screen_height/5))
        screen.blit(start_text, (start_button.center[0] - start_text.get_width()/2, start_button.center[1] - start_text.get_height()/2))
        screen.blit(quiz_text, (quiz_button.center[0] - quiz_text.get_width()/2, quiz_button.center[1] - quiz_text.get_height()/2))
        screen.blit(exit_text, (exit_button.center[0] - exit_text.get_width()/2, exit_button.center[1] - exit_text.get_height()/2))

        #Call the button_clicked method, once for each button, so the program can continue as necessary when a button is pressed
        b1 = button_clicked(start_button, button_width, button_height, mouse, click)
        b2 = button_clicked(quiz_button, button_width, button_height, mouse, click)
        b3 = button_clicked(exit_button, button_width, button_height, mouse, click)

        #Start button pressed, so start the simulation screen
        if b1:
            main_simulation()

        #Quiz button pressed, so start the quiz
        if b2:
            quiz()

        #Exit button pressed, so end the program
        if b3:
            pygame.quit()
            sys.exit()


        #Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        mainClock.tick(60) #The framerate is set to 60 fps; will help when managing the animation later

#Function to call the main simulation screen
def main_simulation():
    screen.fill(screen_background) #Remove all of the previous text and buttons
    pygame.display.set_caption("Photoelectric Effect Simulator - Simulation") #Update the window title

    running_sim = True
    i=1

    while running_sim:

        #Temporary testing values to move a circle from a to b
        start_pos = (700, 50)
        end_pos = (400, 500)

        #Essentially acts as how fast the circle will move; it is how many frames the animation uses. Lower number = faster movement
        #Will be useful later to represent differences in Kinetic Energy of emitted photoelectrons
        steps = 120

        screen.fill(screen_background) #Clear the screen again so the circle's previous position is removed

        #Temporary; just to show where the circle is moving to and from
        pygame.draw.circle(screen, (0,0,0), start_pos, 10)
        pygame.draw.circle(screen, (0,0,0), end_pos, 10)

        #Until the number of steps has been completed, continue to move the circle towards the end position
        if i < steps+1:
            pygame.draw.circle(screen, white, (int(start_pos[0] + ((end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((end_pos[1]-start_pos[1])/steps)*i)), 10)
            print((int(start_pos[0] + ((end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((end_pos[1]-start_pos[1])/steps)*i)))
            i += 1
            print(i)

        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_quiz = False
                    screen.fill(screen_background)
                    pygame.display.set_caption("Photoelectric Effect Simulator - Menu")

        pygame.display.update()
        mainClock.tick(60)


main_menu()

#Old event loop
##while True:
##    pygame.display.update()
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            pygame.quit()
##            sys.exit()
