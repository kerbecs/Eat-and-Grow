"""
------------------------------------------------------------------
                  Eat and Grow Version VI ( The Game)
------------------------------------------------------------------
"""
import schedule
from pygame import display, event, draw, font, mouse
from pygame.time import get_ticks, Clock
import pygame.event
from random import randint
from math import sqrt
from threading import Thread
from time import sleep

class Game:
    colors = ("Green", "Yellow", "Pink", "Purple", "Red", "Brown", "Gray")
    frame_rate = 80
    clock = Clock()
    window_size = None
    window_surface = None
    time = 0
    def __init__(self, window, window_size):
        self.__window = window
        Game.window_surface = window.return_surface()
        self.__dynamic_circle_objects = []
        self.__size_circle_player = 25
        self.running = True
        self.background_color = window.return_actual_bkc()
        self.window_size = window_size
        Game.window_size = window_size
        self.__player_circle_color = Game.chose_color()
        self.__text = "ME"
        self.__text_size = 15
        self.text_font = 'Verdana'
        self.text_color = "Black"
        self.__player_circle_coords = [(self.window_size[0]+self.__size_circle_player)/2, (self.window_size[1]+self.__size_circle_player)/2]
        self.player_circle_speed = [0, 0]
        self.max_speed = 1

    def draw_game(self):
        # this method draws all the objects on the screen
        while self.running:
            Game.window_surface.fill(self.background_color)
            self.handle_events()
            self.move_to_mouse()
            self.move_player_circle()
            self.verify_bound()
            if (get_ticks()//1000) - 5 == Game.time:
                 Game.time += 5
                 Game.create_static_circle(self.__player_circle_coords,self.__size_circle_player)
            StaticCircles.draw_static_circles()
            self.draw_player_circle()
            display.update()
            Game.clock.tick(Game.frame_rate)

    def handle_events(self):
        # this method handles all the possible events of the player
        for ev in event.get():
            if ev.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def chose_color():
        # this method choses a random color
        return Game.colors[randint(0, len(Game.colors)-1)]

    def draw_player_circle(self):
        # this method draw the player's circle
        self.__player_circle = pygame.draw.circle(Game.window_surface, self.__player_circle_color, self.__player_circle_coords, self.__size_circle_player)
        title_font = font.SysFont(self.text_font, self.__text_size, bold=True)
        text_dimension = title_font.size(self.__text)
        Game.window_surface.blit(title_font.render(self.__text, True, self.text_color), (self.__player_circle_coords[0]-text_dimension[0]/2, self.__player_circle_coords[1]-text_dimension[1]/2))

    def x_y_raport(self):
        # this method counts the raport betwen the distance witch x and y need to perform
        try:
            if round(self.__player_circle_coords[0] + self.__size_circle_player) < self.mouse_pos[0]:
                if round(self.__player_circle_coords[1] + self.__size_circle_player) < self.mouse_pos[1]:
                    self.x_y_rap = (self.mouse_pos[0] - (round(self.__player_circle_coords[0] + self.__size_circle_player)))/(
                            self.mouse_pos[1] - (round(self.__player_circle_coords[1]+self.__size_circle_player)))
                elif round(self.__player_circle_coords[1] - self.__size_circle_player) > self.mouse_pos[1]:
                    self.x_y_rap = (self.mouse_pos[0] - (round(self.__player_circle_coords[0] + self.__size_circle_player)))/(
                            round(self.__player_circle_coords[1] - self.__size_circle_player) - self.mouse_pos[1])
            elif round(self.__player_circle_coords[0] - self.__size_circle_player) > self.mouse_pos[0]:
                if round(self.__player_circle_coords[1] + self.__size_circle_player) < self.mouse_pos[1]:
                    self.x_y_rap = (round(self.__player_circle_coords[0] - self.__size_circle_player) - self.mouse_pos[0]) / (
                        self.mouse_pos[1] - (round(self.__player_circle_coords[1]) + self.__size_circle_player))
                elif round(self.__player_circle_coords[1] - self.__size_circle_player) > self.mouse_pos[1]:
                    self.x_y_rap = (round(self.__player_circle_coords[0] - self.__size_circle_player) - self.mouse_pos[0]) / (
                             round(self.__player_circle_coords[1] - self.__size_circle_player) - self.mouse_pos[1])
        except ZeroDivisionError:
            self.x_y_rap = "exception"

    def change_speed(self,nr1, x_mark, y_mark):
        # this method changes the speed direction
        # - nr1 - if we need to modify y speed, nr1 will be 1, if the speed is constant for x and y, nr is 2
        # - x_mark - this is direction for x. + is on right - is on left
        # - y_mark - this is direction for y. + is on down - is on top

        # this if change the y speed
        if nr1 == 1:
            self.player_circle_speed[0] = x_mark * 1
            self.player_circle_speed[1] = (y_mark * 1) / self.x_y_rap
        # this elif doesn't change the speed, which means the speed is constant (1,1)
        elif nr1 == 2:
            self.player_circle_speed[0] = 1 * x_mark
            self.player_circle_speed[1] = 1 * y_mark

    def move_to_mouse(self):
        # this method decide how the player's circle has to move to touch the mouse
        self.mouse_pos = mouse.get_pos()
        self.x_y_raport()

        if self.mouse_pos[0] == round(self.__player_circle_coords[0]): # if the mouse and the circle are vertical equal
            if self.mouse_pos[1] > round(self.__player_circle_coords[1] + self.__size_circle_player): # the mouse is below the circle
                self.change_speed(2, 0, 1)
            elif self.mouse_pos[1] < round(self.__player_circle_coords[1] - self.__size_circle_player): # the mouse is above the circle
                self.change_speed(2, 0, -1)
        elif self.mouse_pos[1] == round(self.__player_circle_coords[1]): # if the mouse and the circle are horizontally equal
            if self.mouse_pos[0] > round(self.__player_circle_coords[0] + self.__size_circle_player): # the mouse is on right of the circle
                self.change_speed(2, 1, 0)
            elif self.mouse_pos[0] < round(self.__player_circle_coords[0] - self.__size_circle_player): # the mouse is on left of the circle
                self.change_speed(2, -1, 0)
        elif self.mouse_pos[0] > round(self.__player_circle_coords[0] + self.__size_circle_player): # the mouse is in the second or 4th dial
            if self.mouse_pos[1] > round(self.__player_circle_coords[1] + self.__size_circle_player): # the mouse is in the 4th dial
                if self.x_y_rap > 1:
                   self.change_speed(1, +1, +1)
                elif self.x_y_rap == 1:
                    self.change_speed(2, +1, +1)
            elif self.mouse_pos[1] < round(self.__player_circle_coords[1] - self.__size_circle_player): # the mouse is in the second dial
                if self.x_y_rap > 1:
                    self.change_speed(1, +1, -1)
                elif self.x_y_rap == 1:
                    self.change_speed(2, +1, -1)

        elif self.mouse_pos[0] < round(self.__player_circle_coords[0] - self.__size_circle_player): # the mouse is in the first or third dial
            if self.mouse_pos[1] > round(self.__player_circle_coords[1] + self.__size_circle_player): # the mouse is in the third dial
                if self.x_y_rap > 1:
                    self.change_speed(1, -1, +1)
                elif self.x_y_rap == 1:
                    self.change_speed(2, -1, +1)
            elif self.mouse_pos[1] < round(self.__player_circle_coords[1] - self.__size_circle_player): # the mouse is in the first dial
                if self.x_y_rap > 1:
                    self.change_speed(1, -1, -1)
                elif self.x_y_rap == 1:
                    self.change_speed(2, -1, -1)

    def move_player_circle(self):
        # this method moves the player's circle
        self.__player_circle_coords[0] += self.player_circle_speed[0]
        self.__player_circle_coords[1] += self.player_circle_speed[1]

    def verify_bound(self):
        # this method verifies if the player's circle doesn't touch the borders. If it does it, it bounds
        if (self.__player_circle_coords[0] <= self.__size_circle_player or self.__player_circle_coords[0] >=
                self.window_size[0] - self.__size_circle_player
                or self.__player_circle_coords[1] <= self.__size_circle_player or self.__player_circle_coords[1] >=
                self.window_size[1] - self.__size_circle_player):
            self.player_circle_speed[0] = -self.player_circle_speed[0]
            self.player_circle_speed[1] = -self.player_circle_speed[1]

    @staticmethod
    def create_static_circle(player_circle_coords, player_circle_size):
        # this method create a static circle if their max number is not reached
        if len(StaticCircles.static_circle_objects) < StaticCircles.max_static_circles:
            StaticCircles(player_circle_coords, player_circle_size)

class StaticCircles:
    spawn_time = 5 # every new static circle will be spawned after this time
    size = (10,20) # these are the possible sizes for every static circle
    color = ("red","green","yellow")
    static_circle_objects = []
    window_size = None
    radius_between_player_circle = 50
    distance_to_border = 20
    window_surface = None
    max_static_circles = 30
    distance_to_another_static_circle = 10

    def __init__(self, player_circle_coords, player_circle_size):
        self.size = StaticCircles.chose_size()
        self.color = StaticCircles.choose_color()
        self.player_circle_coords = player_circle_coords
        self.player_circle_size = player_circle_size
        self.choose_coords()
        StaticCircles.static_circle_objects.append(self)


    @staticmethod
    def chose_size():
        # this method chooses a size randomly for the static circle
        return randint(StaticCircles.size[0], StaticCircles.size[1])
    @staticmethod
    def choose_color():
        # this method chooses a color randomly for the static circle
        return StaticCircles.color[randint(0,len(StaticCircles.color))-1]

    def choose_coords(self):
        # this method chooses good coords for the static circle
        check_player = False #
        check_static_circles = False

        # this loop is to verify if the static circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles):
            self.coords = (randint(self.size + StaticCircles.distance_to_border, self.window_size[0] - self.size -
                                   self.distance_to_border), randint(self.size + StaticCircles.distance_to_border, self.window_size[1] - self.size -
                                   self.distance_to_border))
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()


    def check_coords_player(self):
        # this method checks if the static circle is as far as it needs from the player's circle
        distance_to_player_circle = sqrt((self.player_circle_coords[0] - self.coords[0])**2+(self.player_circle_coords[1]
                                                                            - self.coords[1])**2) - (self.player_circle_size + self.size)
        if distance_to_player_circle < StaticCircles.radius_between_player_circle:
            return False
        else:
            return True

    def check_coords_other_static_circles(self):
        # this method checks if the static circle is as far as it needs from the other static circles
        for static_circle in StaticCircles.static_circle_objects:
            distance_to_other_static_circle = sqrt((self.coords[0] - static_circle.coords[0])**2+(self.coords[1] - static_circle.coords[1])**2)
            if distance_to_other_static_circle <= StaticCircles.distance_to_another_static_circle:
                return False
        return True

    @staticmethod
    # this method draws all the static circles
    def draw_static_circles():
        for circle in StaticCircles.static_circle_objects:
            pygame.draw.circle(StaticCircles.window_surface,circle.color,circle.coords,circle.size)

def start(window, window_size):
    # this method start the game
    # - window - is the window of the game
    # - window_size - is the size of the window
    StaticCircles.window_size = window_size
    StaticCircles.window_surface = window.return_surface()
    game = Game(window, window_size)
    game.draw_game()
