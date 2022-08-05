"""
------------------------------------------------------------------
                  Eat and Grow Version VIII ( The Game)
------------------------------------------------------------------
"""
import schedule
from pygame import display, event, draw, font, mouse
from pygame.time import get_ticks, Clock
import pygame.event
from random import randint
from math import pi, sqrt
from time import sleep

class Game:
    colors = ("Green", "Yellow", "Pink", "Purple", "Red", "Brown", "Gray")
    frame_rate = 80
    minimum_size = 25
    clock = Clock()
    window_surface = None
    time_static_circles = 0
    time_dangerous_circles = 0
    time_delete_dangerous_circles = 0
    time_dynamic_circles = 0
    time_delete_dynamic_circles = 0
    def __init__(self, window, window_size):
        self.__window = window
        Game.window_surface = window.return_surface()
        self.__size_circle_player = Game.minimum_size
        self.running = True
        self.background_color = window.return_actual_bkc()
        self.window_size = window_size
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
            self.get_time()
            self.check_grow_player_circle()
            self.check_dangerous_player_circle()
            self.check_dynamic_circle()
            StaticCircles.draw_static_circles()
            DangerousCircles.draw_dangerous_circles()
            self.draw_player_circle()
            DynamicCircles.draw_dynamic_circles()
            display.update()
            Game.clock.tick(Game.frame_rate)

    def handle_events(self):
        # this method handles all the possible events of the player
        for ev in event.get():
            if ev.type == pygame.QUIT:
                self.running = False

    def get_time(self):
        if (get_ticks() // 1000) - StaticCircles.spawn_time == Game.time_static_circles:
            Game.time_static_circles += StaticCircles.spawn_time
            Game.create_static_circle(self.__player_circle_coords, self.__size_circle_player)
        if (get_ticks() // 1000) - DangerousCircles.time_spawn == Game.time_dangerous_circles:
            Game.time_dangerous_circles += DangerousCircles.time_spawn
            Game.create_dangerous_circle(self.__player_circle_coords, self.__size_circle_player)
        if (get_ticks() // 1000) - DangerousCircles.time_delete == Game.time_delete_dangerous_circles:
            Game.time_delete_dangerous_circles += DangerousCircles.time_delete
            DangerousCircles.delete_dangerous_circles()
        if(get_ticks() // 1000) - DynamicCircles.time_spawn == Game.time_dynamic_circles:
            Game.time_dynamic_circles += DynamicCircles.time_spawn
            Game.create_dynamic_circle(self.__player_circle_coords, self.__size_circle_player)
        if(get_ticks() // 1000) - DynamicCircles.time_delete == Game.time_delete_dynamic_circles:
            Game.time_delete_dynamic_circles += DynamicCircles.time_delete
            DynamicCircles.delete_dynamic_circles()


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

    def check_grow_player_circle(self):
        # this method checks if the player's circle is over a static circle. In this case, the static circle
        # will disappear and the player's circle will grow
        for static_circle in StaticCircles.static_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - static_circle.coords[0])**2 + (self.__player_circle_coords[1] - static_circle.coords[1])**2)
            if distance_between_circles <= self.__size_circle_player - static_circle.size:
                self.grow_player_circle(static_circle.size)
                StaticCircles.static_circle_objects.remove(static_circle)

    def check_dangerous_player_circle(self):
        for dangerous_circle in DangerousCircles.dangerous_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - dangerous_circle.coords[0]) ** 2 + (
                        self.__player_circle_coords[1] - dangerous_circle.coords[1]) ** 2)
            if distance_between_circles - (self.__size_circle_player + dangerous_circle.size) <= -DangerousCircles.dangerous_distance:
                self.__size_circle_player -= self.__size_circle_player*(dangerous_circle.lose_size/100)
                if self.__size_circle_player < Game.minimum_size:
                    self.__size_circle_player = Game.minimum_size

    def check_dynamic_circle(self):
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - dynamic_circle.coords[0]) ** 2 + (
                        self.__player_circle_coords[1] - dynamic_circle.coords[1]) ** 2)
            if distance_between_circles <= dynamic_circle.size and self.__size_circle_player < dynamic_circle.size:
                pygame.quit()
            elif distance_between_circles <= dynamic_circle.size and self.__size_circle_player > dynamic_circle.size:
                self.grow_player_circle(dynamic_circle.size)
                DynamicCircles.dynamic_circle_objects.remove(dynamic_circle)



    def grow_player_circle(self,static_circle_size):
        # this method increases the size of the player's circle
        player_circle_area = Game.area_count(self.__size_circle_player)
        static_circle_area = Game.area_count(static_circle_size)

        player_circle_area += static_circle_area
        self.__size_circle_player = Game.radius_count(player_circle_area)

    @staticmethod
    def chose_color():
        # this method choses a random color
        return Game.colors[randint(0, len(Game.colors)-1)]

    @staticmethod
    def create_static_circle(player_circle_coords, player_circle_size):
        # this method create a static circle if their max number is not reached
        if len(StaticCircles.static_circle_objects) < StaticCircles.max_static_circles:
            StaticCircles(player_circle_coords, player_circle_size)

    @staticmethod
    def create_dangerous_circle(player_circle_coords, player_circle_size):
        # this method create a static circle if their max number is not reached
        if len(DangerousCircles.dangerous_circle_objects) < DangerousCircles.max_dangerous_circles:
            DangerousCircles(player_circle_coords, player_circle_size)

    @staticmethod
    def create_dynamic_circle(player_circle_coords, player_circle_size):
        if len(DynamicCircles.dynamic_circle_objects) < DynamicCircles.maximum_number:
            DynamicCircles(player_circle_coords, player_circle_size)

    @staticmethod
    def area_count(size):
        # this method counts the area of a circle with
        # - size - is the radius of the circle
        return pi * (size**2)

    @staticmethod
    def radius_count(area):
        # this method counts the radius which a circle with this area has
        # - area - is the circle's area
        return sqrt(area/pi)

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
    distance_to_dangerous_circle = 40

    def __init__(self, player_circle_coords, player_circle_size):
        self.size = StaticCircles.chose_size()
        self.color = StaticCircles.choose_color()
        self.player_circle_coords = player_circle_coords
        self.player_circle_size = player_circle_size
        self.choose_coords()
        StaticCircles.static_circle_objects.append(self)

    def choose_coords(self):
        # this method chooses good coords for the static circle
        check_player = False #
        check_static_circles = False
        check_dangerous_circle = False

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
            if not check_dangerous_circle:
                check_dangerous_circle = self.check_coords_dangerous_circles()


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

    def check_coords_dangerous_circles(self):
        # this method checks if the static circle is as far as it needs from the dangerous circles
        for dangerous_circle in DangerousCircles.dangerous_circle_objects:
            distance_to_dangerous_circle = sqrt((self.coords[0] - dangerous_circle.coords[0])**2+(self.coords[1] - dangerous_circle.coords[1])**2)
            if distance_to_dangerous_circle <= StaticCircles.distance_to_dangerous_circle:
                return False
        return True

    @staticmethod
    # this method draws all the static circles
    def draw_static_circles():
        for circle in StaticCircles.static_circle_objects:
            pygame.draw.circle(StaticCircles.window_surface,circle.color,circle.coords,circle.size)

    @staticmethod
    def chose_size():
        # this method chooses a size randomly for the static circle
        return randint(StaticCircles.size[0], StaticCircles.size[1])

    @staticmethod
    def choose_color():
        # this method chooses a color randomly for the static circle
        return StaticCircles.color[randint(0, len(StaticCircles.color)) - 1]


class DangerousCircles:
    window_size = None
    window_surface = None
    size = 20
    color = "Black"
    radius_between_player_circle = 100
    dangerous_distance = 5
    distance_to_border = 20
    max_dangerous_circles = 30
    distance_to_static_circle = 25
    distance_to_another_dangerous_circle = 100
    distance_to_player_circle = 100
    time_spawn = 20
    time_delete = 25
    min_to_be_deleted = 7
    max_number = 10
    min_size_player_circle = 20
    lose_size = (30,90)
    text_color = "White"
    text_font = "Verdana"
    text_size = 13
    dangerous_circle_objects = []

    def __init__(self,player_circle_coords, player_circle_size):
        self.player_circle_coords = player_circle_coords
        self.player_circle_size = player_circle_size
        self.lose_size = self.choose_lose_size()
        self.choose_coords()
        self.lose_size = self.choose_lose_size()
        DangerousCircles.dangerous_circle_objects.append(self)

    def choose_lose_size(self):
        return randint(DangerousCircles.lose_size[0],DangerousCircles.lose_size[1])

    def choose_coords(self):
        # this method chooses good coords for the dangerous circle
        check_player = False #
        check_static_circles = False
        check_dangerous_circles = False

        # this loop is to verify if the dangerous circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles) or (not check_dangerous_circles):
            self.coords = (randint(self.size + DangerousCircles.distance_to_border, self.window_size[0] - self.size -
                                   self.distance_to_border), randint(self.size + DangerousCircles.distance_to_border, self.window_size[1] - self.size -
                                   self.distance_to_border))
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()
            if not check_dangerous_circles:
                check_dangerous_circles = self.check_coords_other_dangerous_circles()

    def check_coords_player(self):
        # this method checks if the dangerous circle is as far as it needs from the player's circle
        distance_to_player_circle = sqrt((self.player_circle_coords[0] - self.coords[0])**2+(self.player_circle_coords[1]
                                                                            - self.coords[1])**2) - (self.player_circle_size + self.size)
        if distance_to_player_circle < DangerousCircles.radius_between_player_circle:
            return False
        else:
            return True

    def check_coords_other_static_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other static circles
        for static_circle in StaticCircles.static_circle_objects:
            distance_to_other_static_circle = sqrt((self.coords[0] - static_circle.coords[0])**2+(self.coords[1] - static_circle.coords[1])**2)
            if distance_to_other_static_circle <= DangerousCircles.distance_to_static_circle:
                return False
        return True

    def check_coords_other_dangerous_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other dangerous circles
        for dangerous_circle in DangerousCircles.dangerous_circle_objects:
            distance_to_other_dangerous_circle = sqrt((self.coords[0] - dangerous_circle.coords[0])**2+(self.coords[1] - dangerous_circle.coords[1])**2)
            if distance_to_other_dangerous_circle <= DangerousCircles.distance_to_another_dangerous_circle:
                return False
        return True
    def add_text(self):
        title_font = font.SysFont(DangerousCircles.text_font, DangerousCircles.text_size, bold=True)
        text_dimension = title_font.size(str(self.lose_size))
        Game.window_surface.blit(title_font.render("-"+str(self.lose_size)+"%", True, DangerousCircles.text_color),
                                             (self.coords[0]-self.size, self.coords[1]-text_dimension[1]/2))
    @staticmethod
    def delete_dangerous_circles():
        if len(DangerousCircles.dangerous_circle_objects) >= 7:
            DangerousCircles.dangerous_circle_objects.pop(randint(0,len(DangerousCircles.dangerous_circle_objects)-1))

    @staticmethod
    # this method draws all the static circles
    def draw_dangerous_circles():
        for circle in DangerousCircles.dangerous_circle_objects:
            pygame.draw.circle(DangerousCircles.window_surface,DangerousCircles.color,circle.coords,DangerousCircles.size)
            circle.add_text()


class DynamicCircles:
    window_size = None
    window_surface = None
    initial_size = (30,80)
    color = ["blue","purple","gray"]
    possible_speed = (-1,-0.4,0.4,1)
    interval_speed = []
    time_spawn = 15
    time_delete = 30
    min_nr_to_delete = 4
    maximum_number = 8
    min_nr_to_be_deleted =4
    distance_to_border = 15
    radius_between_player_circle = 50
    distance_to_another_dynamic_circle = 50
    dynamic_circle_objects = []

    def __init__(self,player_circle_coords, player_circle_size):
        self.player_circle_coords = player_circle_coords
        self.player_circle_size = player_circle_size
        self.size = self.choose_size()
        self.choose_coords()
        self.color = self.choose_color()
        DynamicCircles.generate_all_possible_speed()
        self.speed = self.choose_speed()
        DynamicCircles.draw_dynamic_circles()
        DynamicCircles.dynamic_circle_objects.append(self)

    def choose_size(self):
        return randint(DynamicCircles.initial_size[0],DynamicCircles.initial_size[1])

    def choose_color(self):
        return DynamicCircles.color[randint(0,len(DynamicCircles.color)-1)]

    def choose_coords(self):
        # this method chooses good coords for the dangerous circle
        check_player = False  #
        check_static_circles = False
        check_dangerous_circles = False
        check_dynamic_circles = False

        # this loop is to verify if the dangerous circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles) or (not check_dangerous_circles):
            self.coords = [
            randint(self.size + DynamicCircles.distance_to_border, self.window_size[0] - self.size -
                    self.distance_to_border),
            randint(self.size + DynamicCircles.distance_to_border, self.window_size[1] - self.size -
                    self.distance_to_border)]
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()
            if not check_dangerous_circles:
                check_dangerous_circles = self.check_coords_other_dangerous_circles()
            if not check_dynamic_circles:
                check_dynamic_circles = self.check_coords_other_dynamic_circles()

    def choose_speed(self):
        return [DynamicCircles.interval_speed[randint(0,len(DynamicCircles.interval_speed)-1)],
                                              DynamicCircles.interval_speed[randint(0,len(DynamicCircles.interval_speed)-1)]]

    def check_coords_player(self):
        # this method checks if the dangerous circle is as far as it needs from the player's circle
        distance_to_player_circle = sqrt(
            (self.player_circle_coords[0] - self.coords[0]) ** 2 + (self.player_circle_coords[1]
                                                                     - self.coords[1]) ** 2) - (
                                                self.player_circle_size + self.size)
        if distance_to_player_circle < DangerousCircles.radius_between_player_circle:
            return False
        else:
            return True

    def check_coords_other_static_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other static circles
        for static_circle in StaticCircles.static_circle_objects:
            distance_to_other_static_circle = sqrt(
                (self.coords[0] - static_circle.coords[0]) ** 2 + (self.coords[1] - static_circle.coords[1]) ** 2)
            if distance_to_other_static_circle <= DangerousCircles.distance_to_static_circle:
                return False
        return True

    def check_coords_other_dangerous_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other dangerous circles
        for dangerous_circle in DangerousCircles.dangerous_circle_objects:
            distance_to_other_dangerous_circle = sqrt((self.coords[0] - dangerous_circle.coords[0]) ** 2 + (
                        self.coords[1] - dangerous_circle.coords[1]) ** 2)
            if distance_to_other_dangerous_circle <= dangerous_circle.size + DangerousCircles.distance_to_another_dangerous_circle:
                return False
        return True

    def check_coords_other_dynamic_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other dangerous circles
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            distance_to_other_dynamic_circle = sqrt((self.coords[0] - dynamic_circle.coords[0]) ** 2 + (
                        self.coords[1] - dynamic_circle.coords[1]) ** 2)
            if distance_to_other_dynamic_circle <= DynamicCircles.distance_to_another_dynamic_circle:
                return False
        return True
    def grow_dynamic_circle(self,radius):
        dynamic_circle_area = Game.area_count(self.size)
        new_dynamic_circle_area = dynamic_circle_area + Game.area_count(radius)
        self.size = Game.radius_count(new_dynamic_circle_area)

    @staticmethod
    def check_grow_dynamic_circle():
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            for static_circle in StaticCircles.static_circle_objects:
                distance_between_circles = sqrt((dynamic_circle.coords[0] - static_circle.coords[0])**2 + (dynamic_circle.coords[1] - static_circle.coords[1])**2)
                if distance_between_circles <= dynamic_circle.size:
                    dynamic_circle.grow_dynamic_circle(static_circle.size)
                    StaticCircles.static_circle_objects.remove(static_circle)

        for dynamic_circle1 in DynamicCircles.dynamic_circle_objects:
            for dynamic_circle2 in DynamicCircles.dynamic_circle_objects:
                if dynamic_circle1 != dynamic_circle2 and dynamic_circle1.size > dynamic_circle2.size:
                    distance_between_circles = sqrt((dynamic_circle1.coords[0] - dynamic_circle2.coords[0]) ** 2 + (
                                dynamic_circle1.coords[1] - dynamic_circle2.coords[1]) ** 2)
                    if distance_between_circles <= dynamic_circle1.size:
                        dynamic_circle1.grow_dynamic_circle(dynamic_circle2.size)
                        DynamicCircles.dynamic_circle_objects.remove(dynamic_circle2)

    @staticmethod
    def check_dangerous_circles():
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            for dangerous_circle in DangerousCircles.dangerous_circle_objects:
                distance_between_circles = sqrt((dynamic_circle.coords[0] - dangerous_circle.coords[0]) ** 2 + (
                        dynamic_circle.coords[1] - dangerous_circle.coords[1]) ** 2)
                if distance_between_circles - (
                        dynamic_circle.size + dangerous_circle.size) <= -DangerousCircles.dangerous_distance:
                        dynamic_circle.size -= dynamic_circle.size * (dangerous_circle.lose_size / 100)
                        dynamic_circle.choose_speed()
                if dynamic_circle.size < Game.minimum_size:
                    dynamic_circle.size = Game.minimum_size

    @staticmethod
    # this method draws all the static circles
    def draw_dynamic_circles():
        for circle in DynamicCircles.dynamic_circle_objects:
            pygame.draw.circle(DynamicCircles.window_surface,circle.color,circle.coords,circle.size)
        DynamicCircles.move_dynamic_circle()
        DynamicCircles.check_grow_dynamic_circle()
        DynamicCircles.check_dangerous_circles()

    @staticmethod
    def generate_all_possible_speed():
        x = DynamicCircles.possible_speed[0]
        while (DynamicCircles.possible_speed[0] <= x <= DynamicCircles.possible_speed[1]) or (
                DynamicCircles.possible_speed[2] <= x <= DynamicCircles.possible_speed[3]):
            DynamicCircles.interval_speed.append(x)
            x += 0.1
    @staticmethod
    def move_dynamic_circle():
        for circle in DynamicCircles.dynamic_circle_objects:
            circle.coords[0] += circle.speed[0]
            circle.coords[1] += circle.speed[1]
        DynamicCircles.verify_bound()

    @staticmethod
    def verify_bound():
        # this method verifies if the player's circle doesn't touch the borders. If it does it, it bounds
        for circle in DynamicCircles.dynamic_circle_objects:
            if(circle.coords[0] <= circle.size or circle.coords[0] >= DynamicCircles.window_size[0] - circle.size) \
                    or (circle.coords[1] <= circle.size or circle.coords[1] >= DynamicCircles.window_size[1] - circle.size):
                circle.speed[0] = -circle.speed[0]
                circle.speed[1] = -circle.speed[1]
    @staticmethod
    def delete_dynamic_circles():
        if len(DynamicCircles.dynamic_circle_objects) >= DynamicCircles.min_nr_to_delete:
            DynamicCircles.dynamic_circle_objects.pop(randint(0,len(DynamicCircles.dynamic_circle_objects)-1))

def start(window, window_size):
    # this method start the game
    # - window - is the window of the game
    # - window_size - is the size of the window
    StaticCircles.window_size = window_size
    StaticCircles.window_surface = window.return_surface()
    DangerousCircles.window_size = window_size
    DangerousCircles.window_surface = window.return_surface()
    DynamicCircles.window_size = window_size
    DynamicCircles.window_surface = window.return_surface()
    game = Game(window, window_size)
    game.draw_game()
