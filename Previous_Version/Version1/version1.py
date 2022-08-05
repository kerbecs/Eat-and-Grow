'''
------------------------------------------------------------------
                  Eat and Grow Version I
------------------------------------------------------------------
'''
import sys

import pygame.event
from pygame import display,event,draw,font,Surface,SRCALPHA,mouse

pygame.font.init()
pygame.init()

global window   # this will be the general window

class Window():
# This is a class for the window object

    def __init__(self):
        # set the window's specs
        self.__window_size = (1520,800)
        self.__background_color =  (255,255,255)
        self.__window_title = "Eat and Grow"
        self.running = True

        # set buttons specs
        self.__button_text = ("Play","Exit")
        self.__button_size = (180,90)
        self.__button_font = "Verdana"
        self.__buton_color = (255,0,0)

        # create the window
        self.create_window()

    def create_window(self):
        # this function create the window object
        self.__window = display.set_mode(self.__window_size)
        display.set_caption(self.__window_title)
        self.__window.fill(self.__background_color)

        self.display_window()


        # display the window
    def display_window(self):
        # this function display the window and keep it openned
        # create play and exit buttons
        self.create_surface_nr1()
        self.create_buttons(self.__buton_color,self.__buton_color)
        self.display_surface(self.__surface)
        display.update()

        while self.running:
            for ev in event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.verify_mouse_pos(True)
                self.verify_mouse_pos()
                display.update()




    def create_surface_nr1(self):
        self.__surface_size = (180,230)
        self.__surface = Surface(self.__surface_size,SRCALPHA)

    def display_surface(self,surface):
        self.__window.blit(surface, ((self.__window.get_width() - self.__surface_size[0]) / 2,
                                        (self.__window.get_height() - self.__surface_size[1]) / 2))


    def create_buttons(self,color_buttom_1,color_buttom_2):
        # this function will create the play and exit buttons
        self.rect1 = [(self.__surface_size[0] - self.__button_size[0])/2,(0),
                self.__button_size[0],self.__button_size[1]]
        self.buton1 =  pygame.draw.ellipse(self.__surface,color_buttom_1,self.rect1)
        self.rect2 = [(self.__surface_size[0] - self.__button_size[0]) / 2,
                      (self.__surface_size[1] / 2 + self.__surface_size[1] / 2 - self.__button_size[1]),
                      self.__button_size[0], self.__button_size[1]]
        self.buton2 =  pygame.draw.ellipse(self.__surface,color_buttom_2,self.rect2)
        self.add_text_on_buttons()

    def add_text_on_buttons(self):
        self.text_font = font.SysFont('Verdana',25,bold=True)
        text1_dim = self.text_font.size(self.__button_text[0])
        text2_dim = self.text_font.size(self.__button_text[1])

        self.__button_1 = self.__surface.blit(self.text_font.render(self.__button_text[0],True,(255,255,255)),((self.__surface_size[0]-text1_dim[0])/2
                                                                                             ,(self.__button_size[1]-text1_dim[1])/2))
        self.__button_2 = self.__surface.blit(self.text_font.render(self.__button_text[1], True, (255, 255, 255)),
                            ((self.__surface_size[0] - text2_dim[0]) / 2, (self.__surface_size[1] - self.__button_size[1]/2-text2_dim[1]/2)))


    def verify_mouse_pos(self,close=None):
        mouse_pos = mouse.get_pos()
        a = self.__button_size[0]//2
        b = self.__button_size[1]//2
        scale_y = a / b

        def buton_center_modify(buton):
            return (self.__window_size[0]/2,(self.__window_size[1] - self.__surface_size[1])/2+buton[1])

        def dx_dy_colide(buton_center):
            dx = mouse_pos[0] - buton_center[0]
            dy = (mouse_pos[1] - buton_center[1]) * scale_y
            return [dx,dy,dx*dx + dy*dy]

        def light_button(color1,color2):
            self.create_surface_nr1()
            self.create_buttons(color1,color2)
            self.display_surface(self.__surface)

        buton1_center = buton_center_modify(list(self.__button_1.center))
        buton2_center = buton_center_modify(list(self.__button_2.center))

        dx1,dy1,collide1 = dx_dy_colide(buton1_center)
        dx2,dy2,collide2 = dx_dy_colide(buton2_center)

        if collide1 <= a*a:
            light_button((158,6,6),self.__buton_color)
        elif collide2 <= a*a:
            light_button(self.__buton_color,(158,6,6))
            if close==True:
                pygame.quit()
                sys.exit(0)
        else:
            light_button(self.__buton_color,self.__buton_color)

def main():
    window = Window()



























main()