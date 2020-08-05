import sys, pygame #import pygame, the main library used for graphics

pygame.init() #initialise all of the pygame modules for later use

#Variables for window size
screen_width = 1200
screen_height = 900

white = (255, 255, 255)

screen = pygame.display.set_mode([screen_width, screen_height]) #Creates the screen itself
screen.fill((145, 194, 255)) #Set the background color of the window
pygame.display.set_caption("Photoelectric Effect Simulator V-Alpha") #Set the title of the window

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
def main_menu(mouse, click):
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

    #Exit button pressed, so end the program
    if b3:
        pygame.quit()
        sys.exit()


while True:

    #Get the current mouse position and state of the mouse buttons
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    main_menu(mouse, click) #For testing purposes, just call the menu here

    #Main loop
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
