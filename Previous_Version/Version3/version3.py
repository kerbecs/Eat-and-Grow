'''
------------------------------------------------------------------
                  Eat and Grow Version III
------------------------------------------------------------------
'''
import math
import sys

import pygame.event
from pygame import display,event,draw,font,Surface,SRCALPHA,mouse
from random import  randint
from threading import Thread
from pygame.time import Clock
from math import sqrt

pygame.font.init()
pygame.init()

global window   # this will be the general window

class Window():
    # This is a class for the window object
    window_size = (1520, 800)
    frame_rate = 80
    clock = Clock()

    def __init__(self):
        # set the window's specs
        self.__background_color =  ((255,255,255),(51,51,51))
        self.__actual_background_color = None
        self.__window_title = "Eat and Grow"
        self.running = True

        # set buttons specs
        self.__button_text = ("Play","Exit","Color")
        self.__button_size = (180,90,90,45)
        self.__button_font = "Verdana"
        self.__buton_color = (255,0,0)

        # set the color for a buttom then the mouse touches it
        self.light_color = (158,6,6)

        # set the specs for the square which shows the possile color to change
        self.__square_size = (40,40)

        # set the specs for the title
        self.title_text = "Eat and Grow"
        self.title_color = (255,230,0)
        self.title_size = 130
        self.title_font = 'Jokerman'

        self.stat_moving = False

        # create the window
        self.create_window()

    def create_window(self):
        # this function create the window object and all the objects
        self.__window = display.set_mode(Window.window_size)
        display.set_caption(self.__window_title)
        self.__window.fill(self.__background_color[0])
        self.__actual_background_color = self.__background_color[0]

        # display the window with all the objects
        self.display_window()

    def display_window(self):
        # this function displays the window and keep it openned

        self.create_circles()

        # keep the window open and check all the user's events

        while self.running:
            self.draw()
            self.verify_mouse_pos()
            self.handle_events()
            Circle.move_circle()
            Circle.rebound_circle()
            Circle.touch_circles()
            display.update()

    def handle_events(self):
    # this function handles all the possible events of the player
        for ev in event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.verify_mouse_pos(True)

    def draw(self):
        # this function draws all the objects on the screen

        self.__window.fill(self.__actual_background_color)

        Circle.draw_circle(self.__window)
        # create play and exit buttons
        self.create_surface_nr1()
        self.create_buttons(self.__buton_color,self.__buton_color,self.__buton_color)

        # create the square  for the possible color to switch

        self.square_background_color()

        # add and display the surface
        self.display_surface(self.__surface)

        # display the title
        self.display_title()


    def create_surface_nr1(self):
        # this function creates a surface on which the play and exit button will appear
        self.__surface_size = (180,230)
        self.__surface = Surface(self.__surface_size, SRCALPHA)

    def display_surface(self, surface):
        # this function adds a surface on window
        # - surface - it's the surface which needs to be added on window
        self.__window.blit(surface, ((self.__window.get_width() - self.__surface_size[0]) / 2,
                                        (self.__window.get_height() - self.__surface_size[1]) / 2))


    def create_buttons(self,color_button_1,color_button_2,color_button3):
        # this function will create the play,exit and change color buttons
        # - color_button_1 - is the color for the play button
        # - color_button_2 - is the color for the exit button
        # - color_button_3 - is the color for the change color button

        # rect1 and rect2 will keep the coords for the buttons and their sizes
        self.rect1 = [(self.__surface_size[0] - self.__button_size[0])/2,(0),
                self.__button_size[0],self.__button_size[1]]
        self.buton1 =  pygame.draw.ellipse(self.__surface,color_button_1,self.rect1)
        self.rect2 = [(self.__surface_size[0] - self.__button_size[0]) / 2,
                      (self.__surface_size[1] / 2 + self.__surface_size[1] / 2 - self.__button_size[1]),
                      self.__button_size[0], self.__button_size[1]]
        self.buton2 =  pygame.draw.ellipse(self.__surface,color_button_2,self.rect2)

        self.buton3 = pygame.draw.ellipse(self.__window,color_button3,(1300,600,self.__button_size[2],self.__button_size[3]))

        # add the text after drawing the buttons
        self.add_text_on_buttons()

    def add_text_on_buttons(self):
        # this function add a text for every button

        self.text_font_1 = font.SysFont('Verdana',25,bold=True)
        self.text_font_2 = font.SysFont('Verdana',17,bold=True)

        # count the size for every text
        text1_dim = self.text_font_1.size(self.__button_text[0])
        text2_dim = self.text_font_1.size(self.__button_text[1])
        text3_dim = self.text_font_2.size(self.__button_text[2])

        button_3_center = self.buton3.center

        # add the texts on bottons
        self.__button_1 = self.__surface.blit(self.text_font_1.render(self.__button_text[0],True,(255,255,255)),((self.__surface_size[0]-text1_dim[0])/2
                                                                                             ,(self.__button_size[1]-text1_dim[1])/2))
        self.__button_2 = self.__surface.blit(self.text_font_1.render(self.__button_text[1], True, (255, 255, 255)),
                            ((self.__surface_size[0] - text2_dim[0]) / 2, (self.__surface_size[1] - self.__button_size[1]/2-text2_dim[1]/2)))

        self.__button_3 = self.__window.blit(self.text_font_2.render(self.__button_text[2],True,(255,255,255)),(button_3_center[0]-text3_dim[0]/2,button_3_center[1]-text3_dim[1]/2))


    def verify_mouse_pos(self,close=None):
        # this function verifies if the mouse touches or clicks one of all the buttons
        # - close - this is a parameter which is True if the mouse clicked a button.
        # This parameter is not necessary if the mouse just touches a button

        mouse_pos = mouse.get_pos()
        a1 = self.__button_size[0]//2
        a2 = self.__button_size[2]
        b1 = self.__button_size[1]//2
        b2 = self.__button_size[3]//2

        scale_y_1 = a1 / b1
        scale_y_2 = a2 / b2

        def buton_center_modify(button):
            # this function modifies the button's center, because the play and exit button are on a surface,
            # but we need their central coords for the window's surface
            # - button - is our buton
            return (Window.window_size[0]/2,(Window.window_size[1] - self.__surface_size[1])/2+button[1])

        def dx_dy_colide(button_center):
            # this function counts the dx,dy and colide for the button and returns them
            # - button_center - is a tuple with the coords of a button's center on their original surface

            dx = mouse_pos[0] - button_center[0]
            dy = (mouse_pos[1] - button_center[1]) * scale_y_1
            return [dx,dy,dx*dx + dy*dy]

        def light_button(color1,color2,color3):
            # this function change the button's color then one is touched by mouse
            # - color1 - is the color for the play button
            # - color2 - is the color for the exit button
            # - color3 - is the color for the change color button
            self.create_surface_nr1()
            self.create_buttons(color1,color2,color3)
            self.display_surface(self.__surface)

        buton1_center = buton_center_modify(list(self.__button_1.center))
        buton2_center = buton_center_modify(list(self.__button_2.center))
        buton3_center = self.__button_3.center

        dx1,dy1,collide1 = dx_dy_colide(buton1_center)
        dx2,dy2,collide2 = dx_dy_colide(buton2_center)
        dx3,dy3,collide3 = dx_dy_colide(buton3_center)

        # this part of code decide if a button changes its color and if an action occured
        if collide1 <= a1*a1: # it's for the play button
            light_button(self.light_color,self.__buton_color,self.__buton_color)
        elif collide2 <= a1*a1: # it's for the exit button
            light_button(self.__buton_color,self.light_color,self.__buton_color)
            if close==True: # if it was clicked, then the window closes
                pygame.quit()
                sys.exit(0)
        elif collide3 <= a2*a2: # it's for the change color button
            light_button(self.__buton_color,self.__buton_color,self.light_color)
            if close==True: # if the button was clicked, change the background's color
                self.change_background_color()
        else: # if nothing happened, just draw the buttons as they are
            light_button(self.__buton_color,self.__buton_color,self.__buton_color)

    def change_background_color(self):
        # this function change the background's color

        if self.__actual_background_color == self.__background_color[0]:
            self.__window.fill(self.__background_color[1])
            self.__actual_background_color = self.__background_color[1]
        elif self.__actual_background_color == self.__background_color[1]:
            self.__window.fill(self.__background_color[0])
            self.__actual_background_color = self.__background_color[0]
        self.display_title()
        self.square_background_color()

    def square_background_color(self):
        # this function change the square's color
        buton3_center = self.__button_3.center

        def draw(color):
            # this function colors the square
            self.__square = pygame.draw.rect(self.__window, color,
                                             (buton3_center[0] - self.__square_size[0] / 2,
                                              buton3_center[1] + self.__square_size[1],
                                              self.__square_size[0], self.__square_size[1]))

        # if the background is white,the square must be gray and vice versa
        if(self.__actual_background_color==self.__background_color[0]):
            draw(self.__background_color[1])
        elif(self.__actual_background_color==self.__background_color[1]):
            draw(self.__background_color[0])

    def display_title(self):
        # this function displays the game's title on the window
        self.__title_surface = Surface((680,80),SRCALPHA)

        title_font = font.SysFont(self.title_font,self.title_size,bold=True)
        title_dimension = title_font.size(self.title_text)
        self.__title = self.__title_surface.blit(title_font.render(self.title_text,True,self.title_color),
                                                                   ((self.__title_surface.get_width()-title_dimension[0])/2,
                                                                    (self.__title_surface.get_height()-title_dimension[1])/2))
        self.__window.blit(self.__title_surface,((Window.window_size[0]-self.__title_surface.get_width())/2,110))

    def create_circles(self):
        # this function creates and draws circles
        Circle.selected_circle_number = randint(Circle.circle_numbers[0],Circle.circle_numbers[1])
        for i in range(Circle.selected_circle_number):
            Circle()
        Circle.draw_circle(self.__window)





class Circle:
    # this class is for each circle which is moving on the background

    # there are general specs for every circle
    circle_size = (20,80)
    circle_colors = ("Red","Green","Yellow","Purple","Black","blue","brown")
    circle_coords = Window.window_size
    # it's the number of circles which could appear on the background
    circle_numbers = (6,15)
    selected_circle_number = None
    # this is a list of all created circles
    circle_objects = []

    # the circle moves 2 times faster vertically than horizontally
    speed = (1,2)

    # this is a list of all circles coords, to be sure that one circle can't be drawn on another circle
    all_circles_coords = []


    def __init__(self):
        # in the constructor, the program selects a random size, color and central position(coords of it's center)
        self.size = randint(Circle.circle_size[0],Circle.circle_size[1])
        self.color = Circle.circle_colors[randint(0,len(Circle.circle_colors))-1]
        self.chose_coords()
        self.direction = None
        self.chose_direction()
        Circle.circle_objects.append(self)

    def chose_direction(self):
        # this method chooses coords for a circle but verify that the circle not to be draw over another exiting circle
        while True:
            self.direction = [randint(-1, 2), randint(-2, 3)]
            if self.direction[0] == 0 or self.direction[1] == 0:
                continue
            else:
                break


    def chose_coords(self):
        # this function choses coords for the circle and chekcs if they weren't defined yet

        # these are coords of the circle
        coords = []

        def chose_x_y():
            # this function chose x and y coords
            while True:
                x = randint(self.size, Circle.circle_coords[0] - self.size)
                y = randint(self.size, Circle.circle_coords[1] - self.size)
                for circle in Circle.circle_objects:
                    if math.sqrt((x-circle.coords[0])**2+(y-circle.coords[1])**2) - (self.size + circle.size) <= 10:
                        break
                else:
                    break
            return [x,y]

        # this loop checks if the chosen coords aren't defined yet
        while True:
            self.coords = chose_x_y()
            if tuple(coords) in Circle.all_circles_coords:
                continue
            else:
                break

        Circle.all_circles_coords.append(self.coords)

    @staticmethod
    def draw_circle(surface):
        # this method draws all the circles
        for circle in Circle.circle_objects:
            pygame.draw.circle(surface,circle.color,circle.coords,circle.size,0)

    @staticmethod
    def move_circle():
        # this method move the circles
        for circle in Circle.circle_objects:
            circle.coords[0] += circle.direction[0]
            circle.coords[1] += circle.direction[1]
        Window.clock.tick(Window.frame_rate)

    @staticmethod
    def rebound_circle():
    # this method checks if a circle touches a corner and if it do it, it rebounds
        for circle in Circle.circle_objects:
            if circle.coords[0] + circle.size >= Window.window_size[0] or circle.coords[0] - circle.size  <= 0:
                circle.direction[0] = - circle.direction[0]
            if circle.coords[1] + circle.size  >= Window.window_size[1] or circle.coords[1] - circle.size  <= 0:
                circle.direction[1] = - circle.direction[1]

    @staticmethod
    def touch_circles():
        # this method checks if 2 or more circles touch each over and if they do it, they rebound

        def change_direction(circle):
            # this function changes the direction
            circle.direction[0] = - circle.direction[0]
            circle.direction[1] = - circle.direction[1]

        # this for loop verifies if one circle is touched by one or two circles
        for circle1 in Circle.circle_objects:
            for circle2 in Circle.circle_objects:
                for circle3 in Circle.circle_objects:
                    if circle1 != circle2:
                        if math.sqrt((circle1.coords[0]-circle2.coords[0])**2 +
                                         (circle1.coords[1]-circle2.coords[1])**2) - (circle1.size + circle2 .size) <= 0 and \
                            math.sqrt((circle1.coords[0] - circle3.coords[0]) ** 2 + (circle1.coords[1] - circle3.coords[1]) ** 2) - \
                            (circle1.size + circle3.size) <= 0:
                             change_direction(circle1)
                             break

def main():
    global window
    window = Window()



























main()