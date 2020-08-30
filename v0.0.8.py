import sys, pygame #import pygame, the main library used for graphics
import random
import sqlite3

#DATABASE MANAGEMENT
#====================
def create_table():
    conn = sqlite3.connect("Metals.db") #Connect to the file
    cursor = conn.cursor() #Cursor object to write to

    #Write the sql command to execute, with the necessary fields
    sqlCommand = """
    CREATE TABLE metals (
    name TEXT,
    workFunction FLOAT,
    color TEXT,
    primary key (name)
    )"""

    cursor.execute(sqlCommand) #Execute the command

    conn.commit() #Push the changes to the file
    conn.close() #Close the connection

def add_records():
    conn = sqlite3.connect("Metals.db") #Connect to the file

    #Add records to the file with the necessary values
    #Workfunction given in electron-volts, and colour given as a hex value
    conn.execute("INSERT INTO metals (name, workFunction, color) VALUES ('zinc', 4.3, '727296')");
    conn.execute("INSERT INTO metals (name, workFunction, color) VALUES ('sodium', 2.36, 'D3CCA9')");

    conn.commit() #Push changes to the file
    conn.close() #Close the connection

##create_table()
##add_records()

def query(name):
    name = name.lower()
    conn = sqlite3.connect("Metals.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM metals WHERE name=?', (name, ))

    rows = cursor.fetchall() #fetches all matching values as above

    #Loop through each of the returned values and print them
    for row in rows:
        return row

    conn.close() #close the database connection


#PYGAME MANAGEMENT
#==================

mainClock = pygame.time.Clock()

pygame.init() #initialise all of the pygame modules for later use

#Variables for window size
screen_width = 1200
screen_height = 900

white = (255, 255, 255)
black = (0, 0, 0)
orange = (255,69,0)
yellow = (255,255,0)
screen_background = (145, 194, 255)
slider_background = (0, 148, 255)

screen = pygame.display.set_mode([screen_width, screen_height]) #Creates the screen itself
screen.fill(screen_background) #Set the background color of the window
pygame.display.set_caption("Photoelectric Effect Simulator V-Alpha") #Set the title of the window

def close():
    pygame.quit()
    sys.exit()

## BUTTONS AND SLIDERS INSPIRED BY CODE FROM THE LINK
## https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/

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


##class Slider():
##    def __init__(self, start_val, max_val, min_val, ypos, size):
##        self.start_val = start_val
##        self.max_val = max_val
##        self.min_val = min_val
##        self.xpos = start_val
##        self.ypos = ypos
##        self.size = size #button size
##
##        #static line for the control to slide along
##       # self.track = pygame.draw.line(screen, black, (min_val, self.ypos), (max_val, self.ypos), 1)
##        self.rect = pygame.draw.rect(screen, white, (self.xpos, (self.ypos - self.size[1]/2), self.size[0], self.size[1]))
##
##    def draw(self):
##        self.hover_mouse()
##        self.track = pygame.draw.line(screen, black, (self.min_val, self.ypos), (self.max_val, self.ypos), 1)
##        self.rect = pygame.draw.rect(screen, white, (self.xpos, (self.ypos - self.size[1]/2), self.size[0], self.size[1]))
##        #self.rect.move_ip(self.xpos, self.ypos)
##
##    def hover_mouse(self):
##        pos = pygame.mouse.get_pos()
##        if self.rect.collidepoint(pos):
##            print("HOVER")
##            if pygame.mouse.get_pressed()[0] == 1:
##                print("CLICKED")
##                self.xpos = pos[0] #test this, probably wont work
class Slider():
    def __init__(self, val, max_val, min_val, pos, box_size, button_radius, border_width):
        self.val = val  #start value
        self.max_val = max_val  #Highest value, when slider at right
        self.min_val = min_val  #Lowest value, when slider at left
        self.xpos = pos[0]  #x-location on screen
        self.ypos = pos[1]  #y-location (fixed)
        self.pressed = False  #When the mouse is pressed, the slider can be moved

        self.b_rad = button_radius
        self.box_size = box_size
        self.border_width = border_width

        #STATIC BACKGROUND
        self.surf = pygame.surface.Surface((box_size[0], box_size[1])) #The background "box" for the slider
        self.surf.fill(slider_background)
        pygame.draw.rect(self.surf, white, [0, 0, box_size[0], box_size[1]], self.border_width) #Border for the box
        pygame.draw.rect(self.surf, black, [self.b_rad+self.border_width, (box_size[1]/2) -2, box_size[0] - (2*self.b_rad) -self.border_width, 0], 4) #The track for the slider to move along CHECK THIS

        #MOVING SLIDER
        self.button_surf = pygame.surface.Surface((2*self.b_rad, 2*self.b_rad))
        self.button_surf.fill(slider_background)

        ##MAKE THE COLORS CHANGEABLE LATER?
        pygame.draw.circle(self.button_surf, white, (self.b_rad, self.b_rad), self.b_rad, 0)
        pygame.draw.circle(self.button_surf, orange, (self.b_rad, self.b_rad), int((3*self.b_rad)/4), 0)

    def draw(self):
        surf = self.surf.copy()

        pos = (self.border_width+self.b_rad+int((self.val-self.min_val) / (self.max_val-self.min_val)*(self.box_size[0]-(2*self.b_rad)-(2*self.border_width))), self.box_size[1]/2 -2) #check the math here
        self.button_rect = self.button_surf.get_rect(center = pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)

        screen.blit(surf, (self.xpos, self.ypos))

    def update(self):
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - self.b_rad) / (self.box_size[0]-(2*self.b_rad)) * (self.max_val - self.min_val) + self.min_val

        if self.val < self.min_val:
            self.val = self.min_val
        if self.val > self.max_val:
            self.val = self.max_val

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


    #test_slider = Slider(10, 200, 10, 200, (10, 20))
    test_slider = Slider(20, 200, 10, (200,200), (500, 100), 20, 5)

    #Waiting for a button to be pressed
    while True:

        #Blit the text objects to the screen in the necessary positions
        screen.blit(title, ((screen_width/2)-(title.get_width()/2), screen_height/5))
        for button in buttons:
            button.draw()

        test_slider.draw()

        #Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if test_slider.button_rect.collidepoint(pos):
                    test_slider.pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                test_slider.pressed = False

        if test_slider.pressed:
            test_slider.update()

        pygame.display.update()
        mainClock.tick(60) #The framerate is set to 60 fps; will help when managing the animation later

#The Planck constant (h) is 6.63x10^-34 Js = 4.14x10^-15 eVs
#E_k(max) = hf - [work function]
#f = c/lambda
global planck_constant
##planck_constant = 6.63*10**-34
planck_constant = 4.14*10**-15

class Photon:
    def __init__(self, wavelength, end_pos):
        self.wavelength = wavelength
        self.end_pos = end_pos
        self.frequency = 3*10**8/self.wavelength
        self.reached_end = False

    def draw(self, start_pos, i):
        steps = 120

        pygame.draw.circle(screen, yellow, self.end_pos, 10)

        if i < steps+1:
            pygame.draw.circle(screen, white, (int(start_pos[0] + ((self.end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((self.end_pos[1]-start_pos[1])/steps)*i)), 10)
            ##print((int(start_pos[0] + ((self.end_pos[0]-start_pos[0])/steps)*i), int(start_pos[1] + ((self.end_pos[1]-start_pos[1])/steps)*i)))
            i += 1
        else:
            self.reached_end = True
            ##kinetic_energy = (planck_constant * self.frequency) - float(query("Zinc")[1])
            ##print("Kinetic of photoelectron: ", (planck_constant * self.frequency) - float(query("Zinc")[1]))

            ##photoelectron_1 = PhotoElectron(kinetic_energy, self.end_pos, (self.end_pos[0], 900))

            ##return photoelectron_1

        return i

    def get_data(self):
        kinetic_energy = (planck_constant * self.frequency) - float(query("zinc")[1]) #may need method of getting active metal for here
        print(kinetic_energy)
        return self.end_pos, kinetic_energy

class PhotoElectron:
    def __init__(self, kinetic_energy, start_pos, end_pos):
        self.kinetic_energy = kinetic_energy
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self, n):
        steps = int(120 / self.kinetic_energy) #very rough approximation - improve this later

        if n < steps + 1:
            pygame.draw.circle(screen, orange, (int(self.start_pos[0] + ((self.end_pos[0]-self.start_pos[0])/steps)*n), int(self.start_pos[1] + ((self.end_pos[1]-self.start_pos[1])/steps)*n)), 10)
            n += 1

        return n

photon_1 = Photon(200*10**-9, (random.randrange(35, 75), random.randrange(625, 865)))
photon_2 = Photon(300*10**-9, (random.randrange(35, 75), random.randrange(625, 865)))

photoelectron_1 = PhotoElectron(1, (0,0), (0,0))
photoelectron_2 = PhotoElectron(1, (0,0), (0,0))

#Function to call the main simulation screen
def main_simulation():
    screen.fill(screen_background) #Remove all of the previous text and buttons
    pygame.display.set_caption("Photoelectric Effect Simulator - Simulation") #Update the window title

    selected_metal = "zinc" #this will be changable in the menu later
    metal_data = query(selected_metal) #Given as (name, work function, hex color)
    metal_color = pygame.Color("#"+metal_data[2])

    running_sim = True
    i = 1
    n=1
    m=1
    ##i2 = 1

    wavelength_slider = Slider(20, 200, 10, (20,20), (500, 100), 20, 5)
    sliders = [wavelength_slider]

    while running_sim:

        #Temporary testing values to move a circle from a to b
        start_pos = (400, 550)

        screen.fill(screen_background) #Clear the screen again so the circle's previous position is removed

        for slider in sliders:
            slider.draw()

        metal_plate = pygame.draw.rect(screen, metal_color, (30, 620, 50, 250))

        pygame.draw.line(screen, (0,0,0), (80, 620), (400, 550))
       ##pygame.draw.line(screen, (0,0,0), (80, 745), (400, 550))
        pygame.draw.line(screen, (0,0,0), (80, 870), (400, 550))
        lamp = pygame.draw.circle(screen, (255,255,255), (400, 550), 15)

##        #intensity = 2
##        #photon_queue = [photon_1, photon_2]
##        #photoelectron_queue = [photoelectron_1, photoelectron_2]
##
##        for x in range(intensity):
##            if not photon_queue[x].reached_end:
##                i = photon_queue[x].draw(start_pos, i)
##
##            else:
##                a = photon_queue[x].get_data()
##                #photon_queue.pop(x)
##                print(a)
##                photoelectron_queue[x] = PhotoElectron(a[1], a[0], (900, a[0][1]))
##                n = photoelectron_1.draw(n)
##                m = photoelectron_2.draw(m)

        #Drawing the photons
        if not photon_1.reached_end:
            i = photon_1.draw(start_pos, i)

        else:
            a = photon_1.get_data()
            photoelectron_1 = PhotoElectron(a[1], a[0], (900, a[0][1]))
            n = photoelectron_1.draw(n)

        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            #If the user presses escape, return them to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
##                    for photon in photon_queue:
##                        photon.reached_end = False
                    photon_1.reached_end = False
                    running_sim = False
                    screen.fill(screen_background)
                    pygame.display.set_caption("Photoelectric Effect Simulator - Menu")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for slider in sliders:
                    if slider.button_rect.collidepoint(pos):
                        slider.pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.pressed = False

        for slider in sliders:
            if slider.pressed:
                slider.update()

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
