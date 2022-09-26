"""
------------------------------------------------------------------
                  Eat and Grow Version XI ( The Game)
------------------------------------------------------------------
"""
import sys
from pygame import display, event, draw, font, mouse
from pygame.time import get_ticks, Clock
import pygame.event
from random import randint
from math import pi, sqrt

class Game:
    colors = ("Green", "Yellow", "Pink", "Purple", "Red", "Brown", "Gray")
    frame_rate = 80
    minimum_size = 25
    minimum_text_size = 15
    clock = Clock()
    window_surface = None
    time_static_circles = 0
    time_dangerous_circles = 0
    time_delete_dangerous_circles = 0
    time_dynamic_circles = 0
    time_delete_dynamic_circles = 0
    time_change_speed = 0
    last_time = 0
    wait_exit_time = 3

    # this attribute is to verify if the mouse changes its old position. If it doesn't it, the circle will not move after the old mouse position
    # This is util if the mouse is out the window and has to rebound or if the circles touches the mouse, but the player doesn't change the mouse position.
    # In this last case, the circle will move straight on
    old_position_mouse = []

    def __init__(self, window, __window_size):
        # window's specs
        self.__window = window
        Game.window_surface = window.return_surface()
        self.__window_size = __window_size
        self.__background_color = window.return_actual_bkc()

        # player's circle specs
        self.__size_circle_player = Game.minimum_size
        self.__player_circle_coords = [(self.__window_size[0]+self.__size_circle_player)/2, (self.__window_size[1]+self.__size_circle_player)/2]
        self.__text = "ME"
        self.__text_size= 15
        self.__text_size_font = "Jokerman"
        self.player_circle_speed = [0, 0]
        self.max_speed = 1
        self.player_circle_player_is_alive = True

        self.__running = True
        self.__player_circle_color = Game.choose_color()

        # text's specs
        self.__text_size_color = "aqua"
        self.__text_font = 'Verdana'
        self.__text_color = "Black"

        # this attribute is needed to verify the time the program start, because all the circles are spawned
        # in a certain time, and if the player loses and returns to the menu and again starts the game,
        # the running time of programme will change, and we need to count the time the game started again
        self.time_exit = 0

        # this attribute verifies if the circle touches an edge. If it does it, this attribute will not allow to player's circle to move after the mouse
        self.bound = False

        Game.count_time()

    def draw_game(self):
        # this method draws all the objects on the screen
        
        while self.__running:
            Game.window_surface.fill(self.__background_color)
            Game.handle_events()
            self.move_player_circle()
            self.move_to_mouse()
            self.verify_bound()
            self.get_time()
            self.check_grow_player_circle()
            self.check_dangerous_player_circle()
            StaticCircles.draw_static_circles()
            DangerousCircles.draw_dangerous_circles()
            if self.player_circle_player_is_alive:
                # these methods must be executed only if the player is still alive
                self.draw_player_circle()
                self.check_dynamic_circle()
            else:
                # this statement just assures that the game will run for a few seconds after the player has lost
                if self.time_exit + self.wait_exit_time > get_ticks()/1000:
                    pass
                else:
                    # this statement ends the game
                    self.__running = False
                    Game.clear()
            DynamicCircles.draw_dynamic_circles()
            display.update()
            Game.clock.tick(Game.frame_rate)

    def get_time(self):
        # this method assures that every different circle will be spawned and deleted after a certain defined time
        
        if ((get_ticks() - Game.last_time) // 1000) - StaticCircles.spawn_time == Game.time_static_circles:
            Game.time_static_circles += StaticCircles.spawn_time
            Game.create_static_circle(self.__player_circle_coords, self.__size_circle_player)
        if ((get_ticks() - Game.last_time) // 1000) - DangerousCircles.time_spawn == Game.time_dangerous_circles:
            Game.time_dangerous_circles += DangerousCircles.time_spawn
            Game.create_dangerous_circle(self.__player_circle_coords, self.__size_circle_player)
        if ((get_ticks() - Game.last_time) // 1000) - DangerousCircles.time_delete == Game.time_delete_dangerous_circles:
            Game.time_delete_dangerous_circles += DangerousCircles.time_delete
            DangerousCircles.delete_dangerous_circles()
        if((get_ticks() - Game.last_time) // 1000) - DynamicCircles.time_spawn == Game.time_dynamic_circles:
            Game.time_dynamic_circles += DynamicCircles.time_spawn
            Game.create_dynamic_circle(self.__player_circle_coords, self.__size_circle_player)
        if((get_ticks() - Game.last_time) // 1000) - DynamicCircles.time_delete == Game.time_delete_dynamic_circles:
            Game.time_delete_dynamic_circles += DynamicCircles.time_delete
            DynamicCircles.delete_dynamic_circles()
        if((get_ticks() - Game.last_time) // 1000) - DynamicCircles.time_to_change_speed == Game.time_change_speed:
            Game.time_change_speed += DynamicCircles.time_to_change_speed
            if len(DynamicCircles.dynamic_circle_objects) > 0:
                DynamicCircles.dynamic_circle_objects[randint(1,len(DynamicCircles.dynamic_circle_objects))-1].change_speed()

    def draw_player_circle(self):
        # this method draws the player's circle
        
        self.__player_circle = pygame.draw.circle(Game.window_surface, self.__player_circle_color, self.__player_circle_coords, self.__size_circle_player)
        self.add_text()

    def x_y_raport(self):
        # this method counts the raport between the distance which x and y need to perform.
        # The player's circle has to move with a certain speed to touch the mouse
        
        try:
            distance = sqrt((self.__player_circle_coords[0]-self.mouse_pos[0])**2+(self.__player_circle_coords[1]+self.mouse_pos[1])**2)
            self.x_y_rap = abs(round(((self.mouse_pos[0] - self.__player_circle_coords[0])/distance)/((self.mouse_pos[1] - self.__player_circle_coords[1])/distance),5))
        except ZeroDivisionError:
            self.x_y_rap = "exception"

    def change_speed(self,nr1, x_mark, y_mark):
        # this method changes the speed direction
        # - nr1 - if we need to modify y speed, nr1 will be 1, if the speed is constant for x and y, nr is 2
        # - x_mark - this is direction for x. + is on right - is on left
        # - y_mark - this is direction for y. + is on down - is on top

        # this if changes y or x speed
        if nr1 == 1:
            self.player_circle_speed[0] = x_mark * 1
            try:
                # if the player's circle has to move more on x, y will be lower
                if self.x_y_rap > 1:
                    self.player_circle_speed[0] = x_mark * 1
                    self.player_circle_speed[1] = (y_mark * 1) / self.x_y_rap
                # if the player's circle has to move more on y, the x will be lower
                elif self.x_y_rap < 1:
                    self.player_circle_speed[0] = (x_mark * 1)*self.x_y_rap
                    self.player_circle_speed[1] = (y_mark * 1)
            except ZeroDivisionError:
                self.player_circle_speed[1] = "ERROR"

        # this elif does the speed constant: (1,1) or (0,1) or (1,0)
        elif nr1 == 2:
            self.player_circle_speed[0] = 1 * x_mark
            self.player_circle_speed[1] = 1 * y_mark

    def move_to_mouse(self):
        # this method decide how the player's circle has to move to touch the mouse

        self.mouse_pos = mouse.get_pos()
        self.x_y_raport()

        # this statement checks how the circle has to move to arrive to the mouse.
        # this statement is executed only if:
        # - the mouse is not in the center of the player's circle
        # - the circle doesn't touch an edge of the window
        # - the mouse changes its position
        if round(self.__player_circle_coords[0]) != self.mouse_pos[0] and round(self.__player_circle_coords[1]) != \
                self.mouse_pos[1] and self.bound == False and self.mouse_pos != Game.old_position_mouse:
            # if the mouse is between the center coords of the player's cirle
            if round(self.__player_circle_coords[0] - self.__size_circle_player) <= self.mouse_pos[0] <= round(self.__player_circle_coords[0] + self.__size_circle_player):
                if self.mouse_pos[1] > self.__player_circle_coords[1]: # mouse is below the circle
                    self.change_speed(2,0,1)
                elif self.mouse_pos[0] < self.__player_circle_coords[0]: # mouse is above the circle
                    self.change_speed(2,0,-1)

            elif self.mouse_pos[0] > round(self.__player_circle_coords[0] + self.__size_circle_player):  # the mouse is in the second or 4th dial
                if self.mouse_pos[1] > round(self.__player_circle_coords[1]):  # the mouse is in the 4th dial
                    if self.x_y_rap > 1 or self.x_y_rap < 1:
                        self.change_speed(1, +1, +1)
                    elif self.x_y_rap == 1:
                        self.change_speed(2, +1, +1)
                elif self.mouse_pos[1] < round(self.__player_circle_coords[1]):  # the mouse is in the second dial
                    if self.x_y_rap > 1 or self.x_y_rap < 1:
                        self.change_speed(1, +1, -1)
                    elif self.x_y_rap == 1:
                        self.change_speed(2, +1, -1)
                elif round(self.__player_circle_coords[1] + self.__size_circle_player/4) >= self.mouse_pos[1] >= round(self.__player_circle_coords[1] - self.__size_circle_player/4): # the
                    # mouse is horizontal
                    self.change_speed(2,1,0)

            if self.mouse_pos[0] < round(self.__player_circle_coords[0]):  # the mouse is in the first or third dial
                if self.mouse_pos[1] > round(self.__player_circle_coords[1]):  # the mouse is in the third dial
                    if self.x_y_rap > 1 or self.x_y_rap < 1:
                        self.change_speed(1, -1, +1)
                    elif self.x_y_rap == 1:
                        self.change_speed(2, -1, +1)
                elif self.mouse_pos[1] < round(self.__player_circle_coords[1]):  # the mouse is in the first dial
                    if self.x_y_rap > 1 or self.x_y_rap < 1:
                        self.change_speed(1, -1, -1)
                    elif self.x_y_rap == 1:
                        self.change_speed(2, -1, -1)
                elif round(self.__player_circle_coords[1] - self.__size_circle_player/4) <= self.mouse_pos[1] <= round(self.__player_circle_coords[1] + self.__size_circle_player/4): # the
                    # mouse is horizontal
                    self.change_speed(2,-1,0)
        Game.old_position_mouse = self.mouse_pos
    def move_player_circle(self):
        # this method moves the player's circle
        self.__player_circle_coords[0] += self.player_circle_speed[0]
        self.__player_circle_coords[1] += self.player_circle_speed[1]

    def verify_bound(self):
        # this method verifies if the player's circle doesn't touch the borders. If it does it, it bounds

        if (self.__player_circle_coords[0] <= self.__size_circle_player or self.__player_circle_coords[0] >=
                self.__window_size[0] - self.__size_circle_player
                or self.__player_circle_coords[1] <= self.__size_circle_player or self.__player_circle_coords[1] >=
                self.__window_size[1] - self.__size_circle_player):
            self.player_circle_speed[0] = -self.player_circle_speed[0]
            self.player_circle_speed[1] = -self.player_circle_speed[1]
            self.move_player_circle()
            self.bound = True
        # id the circle doesn't touch any edges, it can move after the mouse normally
        else:
            self.bound = False

    def check_grow_player_circle(self):
        # this method checks if the player's circle is over a static circle. In this case, the static circle
        # will disappear and the player's circle will grow
        
        for static_circle in StaticCircles.static_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - static_circle.coords[0])**2 + (self.__player_circle_coords[1] - static_circle.coords[1])**2)
            if distance_between_circles <= self.__size_circle_player - static_circle.size:
                self.grow_player_circle(static_circle.size)
                StaticCircles.static_circle_objects.remove(static_circle)

    def check_dangerous_player_circle(self):
        # this method checks if the player's circle touches a dangerous circle. If it does it, the player's circle loses on weight
        
        for dangerous_circle in DangerousCircles.dangerous_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - dangerous_circle.coords[0]) ** 2 + (
                        self.__player_circle_coords[1] - dangerous_circle.coords[1]) ** 2)
            if distance_between_circles - (self.__size_circle_player + dangerous_circle.size) <= -DangerousCircles.dangerous_distance:
                self.__size_circle_player -= self.__size_circle_player*(dangerous_circle.lose_size/100)
                if self.__size_circle_player < Game.minimum_size:
                    self.__size_circle_player = Game.minimum_size

    def check_dynamic_circle(self):
        # this method checks the situation when the player's circle touches too much a dynamic circle.
        # In this case, the player's circle must grow or be eaten and the player loses.
        
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            distance_between_circles = sqrt((self.__player_circle_coords[0] - dynamic_circle.coords[0]) ** 2 + (
                        self.__player_circle_coords[1] - dynamic_circle.coords[1]) ** 2)
            if distance_between_circles <= dynamic_circle.size and self.__size_circle_player < dynamic_circle.size:
                dynamic_circle.grow_dynamic_circle(self.__size_circle_player)
                self.player_circle_player_is_alive = False
                self.time_exit = get_ticks()/1000
            elif distance_between_circles <= self.__size_circle_player - dynamic_circle.size//2 and self.__size_circle_player > dynamic_circle.size:
                self.grow_player_circle(dynamic_circle.size)
                DynamicCircles.dynamic_circle_objects.remove(dynamic_circle)

    def grow_player_circle(self,static_circle_size):
        # this method increases the size of the player's circle
        
        player_circle_area = Game.area_count(self.__size_circle_player)
        static_circle_area = Game.area_count(static_circle_size)

        player_circle_area += static_circle_area
        self.__size_circle_player = Game.radius_count(player_circle_area)

    def add_text(self):
        # this method add the texts on the player's circle and adjusts their sizes
        
        raport = Game.minimum_text_size / Game.minimum_size
        self.__text_size = round(self.__size_circle_player * raport)
        title_font = font.SysFont(self.__text_font, self.__text_size, bold=True)
        text_dimension = title_font.size(self.__text)
        Game.window_surface.blit(title_font.render(self.__text, True, self.__text_color),
                                 (self.__player_circle_coords[0]-text_dimension[0]/2, self.__player_circle_coords[1]-0.7*text_dimension[1]))
        title_font = font.SysFont(self.__text_size_font, self.__text_size, bold=True)
        text_dimension = title_font.size(str(round(self.__size_circle_player)))
        Game.window_surface.blit(title_font.render(str(round(self.__size_circle_player)), True, self.__text_size_color),
                                 (self.__player_circle_coords[0]-text_dimension[0]/2, self.__player_circle_coords[1]+0.3*text_dimension[1]))


    @staticmethod
    def choose_color():
        # this method chooses a random color
    
        return Game.colors[randint(0, len(Game.colors)-1)]

    @staticmethod
    def handle_events():
        # this method handles all the possible events of the player
        
        for ev in event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

    @staticmethod
    def create_static_circle(__player_circle_coords, player_circle_size):
        # this method creates a static circle if their max number is not reached
        
        if len(StaticCircles.static_circle_objects) < StaticCircles.max_static_circles:
            StaticCircles(__player_circle_coords, player_circle_size)

    @staticmethod
    def create_dangerous_circle(__player_circle_coords, player_circle_size):
        # this method creates a static circle if their max number is not reached
        
        if len(DangerousCircles.dangerous_circle_objects) < DangerousCircles.max_dangerous_circles:
            DangerousCircles(__player_circle_coords, player_circle_size)

    @staticmethod
    def create_dynamic_circle(__player_circle_coords, player_circle_size):
        # this method creates a dynamic circles if their max number is not reached
        
        if len(DynamicCircles.dynamic_circle_objects) < DynamicCircles.maximum_number:
            DynamicCircles(__player_circle_coords, player_circle_size)

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

    @staticmethod
    def count_time():
        # this method counts the time the game runs
        
        Game.last_time = get_ticks()

    @staticmethod
    def clear():
        # this method deletes all the created circles and resets the time passed
        
        while len(StaticCircles.static_circle_objects) != 0:
            StaticCircles.static_circle_objects.pop()
        while len(DynamicCircles.dynamic_circle_objects) != 0:
            DynamicCircles.dynamic_circle_objects.pop()
        while len(DangerousCircles.dangerous_circle_objects) != 0:
            DangerousCircles.dangerous_circle_objects.pop()
        Game.time_static_circles = 0
        Game.time_dangerous_circles = 0
        Game.time_delete_dangerous_circles = 0
        Game.time_dynamic_circles = 0
        Game.time_delete_dynamic_circles = 0
        Game.time_change_speed = 0


class StaticCircles:
    # this class is for all the static circles. The static circles just are staying
    # and if a player touches them too much, the player's wins weight
    
    spawn_time = 3 # every new static circle will be spawned after this time
    size = (10,20) # these are the possible sizes for every static circle
    color = ("red","green","yellow")
    static_circle_objects = []
    window_size = None
    radius_between_player_circle = 50
    distance_to_border = 20
    window_surface = None
    max_static_circles = 40
    distance_to_another_static_circle = 10
    distance_to_dangerous_circle = 40

    def __init__(self, __player_circle_coords, player_circle_size):
        self.size = StaticCircles.chose_size()
        self.color = StaticCircles.choose_color()
        self.__player_circle_coords = __player_circle_coords
        self.player_circle_size = player_circle_size
        self.choose_coords()
        StaticCircles.static_circle_objects.append(self)

    def choose_coords(self):
        # this method chooses good coords for the static circle
        
        check_player = False
        check_static_circles = False
        check_dangerous_circle = False

        # this loop is to verify if the static circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles):
            self.coords = (randint(self.size + StaticCircles.distance_to_border, StaticCircles.window_size[0] - self.size -
                                   self.distance_to_border), randint(self.size + StaticCircles.distance_to_border, StaticCircles.window_size[1] - self.size -
                                   self.distance_to_border))
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()
            if not check_dangerous_circle:
                check_dangerous_circle = self.check_coords_dangerous_circles()


    def check_coords_player(self):
        # this method checks if the static circle is as far as it needs from the player's circle
        
        distance_to_player_circle = sqrt((self.__player_circle_coords[0] - self.coords[0])**2+(self.__player_circle_coords[1]
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
    def draw_static_circles():
        # this method draws all the static circles

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
    # this class is for dangerous circles. These circles are just staying and if the player's circle
    # touches them too much, it loses on weight
    __window_size = None
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
    time_spawn = 17
    time_delete = 28
    min_to_be_deleted = 7
    max_number = 10
    min_size_player_circle = 20
    lose_size = (20,70)
    __text_color = "White"
    __text_font = "Verdana"
    text_size = 13
    dangerous_circle_objects = []

    def __init__(self,__player_circle_coords, player_circle_size):
        self.__player_circle_coords = __player_circle_coords
        self.player_circle_size = player_circle_size
        self.lose_size = DangerousCircles.choose_lose_size()
        self.choose_coords()
        DangerousCircles.dangerous_circle_objects.append(self)

    def choose_coords(self):
        # this method chooses good coords for the dangerous circle
        
        check_player = False 
        check_static_circles = False
        check_dangerous_circles = False

        # this loop is to verify if the dangerous circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles) or (not check_dangerous_circles):
            self.coords = (randint(self.size + DangerousCircles.distance_to_border, DangerousCircles.window_size[0] - self.size -
                                   self.distance_to_border), randint(self.size + DangerousCircles.distance_to_border, DangerousCircles.window_size[1] - self.size -
                                   self.distance_to_border))
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()
            if not check_dangerous_circles:
                check_dangerous_circles = self.check_coords_other_dangerous_circles()

    def check_coords_player(self):
        # this method checks if the dangerous circle is as far as it needs from the player's circle
        
        distance_to_player_circle = sqrt((self.__player_circle_coords[0] - self.coords[0])**2+(self.__player_circle_coords[1]
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
        # this method add the text which shows how much the dangerous circle can affect the player's circle size
        
        title_font = font.SysFont(DangerousCircles.__text_font, DangerousCircles.text_size, bold=True)
        text_dimension = title_font.size(str(self.lose_size))
        Game.window_surface.blit(title_font.render("-"+str(self.lose_size)+"%", True, DangerousCircles.__text_color),
                                             (self.coords[0]-self.size, self.coords[1]-text_dimension[1]/2))
    @staticmethod
    def delete_dangerous_circles():
        # this method checks if there are enough circles to start removing one of them
        
        if len(DangerousCircles.dangerous_circle_objects) >= DangerousCircles.min_to_be_deleted:
            DangerousCircles.dangerous_circle_objects.pop(randint(0,len(DangerousCircles.dangerous_circle_objects)-1))

    @staticmethod
    def draw_dangerous_circles():
        # this method draws all the static circles

        for circle in DangerousCircles.dangerous_circle_objects:
            pygame.draw.circle(DangerousCircles.window_surface,DangerousCircles.color,circle.coords,DangerousCircles.size)
            circle.add_text()
            
    @staticmethod
    def choose_lose_size():
        # this method chooses a size which the player's circle will lose randomly if it touches a dangerous circle
        
        return randint(DangerousCircles.lose_size[0],DangerousCircles.lose_size[1])

class DynamicCircles:
    # this class is for the dynamic circles. Dynamic circles are moving all the time, they can grow,
    # lose on weight, eat each others and eat the player's circle
    
    window_size = None
    window_surface = None
    
    # these are ranges of possible size,color, and speed of these circles
    initial_size = (30,110)
    color = ["blue","purple","gray"]
    possible_speed = (-1,-0.4,0.4,1)
    interval_speed = []
    
    time_spawn = 12
    time_delete = 30
    min_nr_to_delete = 5
    maximum_number = 8
    min_nr_to_be_deleted =4
    distance_to_border = 15
    radius_between_player_circle = 50
    distance_to_another_dynamic_circle = 50
    dynamic_circle_objects = []
    time_to_change_speed = 6

    def __init__(self,__player_circle_coords, player_circle_size):
        self.__player_circle_coords = __player_circle_coords
        self.player_circle_size = player_circle_size
        self.size = DynamicCircles.choose_size()
        self.choose_coords()
        self.color = DynamicCircles.choose_color()
        DynamicCircles.generate_all_possible_speed()
        self.speed = DynamicCircles.choose_speed()
        DynamicCircles.draw_dynamic_circles()
        DynamicCircles.dynamic_circle_objects.append(self)

    def choose_coords(self):
        # this method chooses good coords for the dangerous circle

        check_player = False
        check_static_circles = False
        check_dangerous_circles = False
        check_dynamic_circles = False

        # this loop is to verify if the dangerous circle is as far as it needs from the player's circle
        # and from other existing static circles
        while (not check_player) or (not check_static_circles) or (not check_dangerous_circles):
            self.coords = [
            randint(self.size + DynamicCircles.distance_to_border, DangerousCircles.window_size[0] - self.size -
                    self.distance_to_border),
            randint(self.size + DynamicCircles.distance_to_border, DangerousCircles.window_size[1] - self.size -
                    self.distance_to_border)]
            if not check_player:
                check_player = self.check_coords_player()
            if not check_static_circles:
                check_static_circles = self.check_coords_other_static_circles()
            if not check_dangerous_circles:
                check_dangerous_circles = self.check_coords_other_dangerous_circles()
            if not check_dynamic_circles:
                check_dynamic_circles = self.check_coords_other_dynamic_circles()

    def change_speed(self):
        number = randint(0,1)
        self.speed[number] = -self.speed[number]

    def check_coords_player(self):
        # this method checks if the dangerous circle is as far as it needs from the player's circle

        distance_to_player_circle = sqrt(
            (self.__player_circle_coords[0] - self.coords[0]) ** 2 + (self.__player_circle_coords[1]
                                                                     - self.coords[1]) ** 2) - (
                                                self.player_circle_size + self.size)
        if distance_to_player_circle < self.size + DangerousCircles.radius_between_player_circle:
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
            if distance_to_other_dangerous_circle <= dangerous_circle.size + self.size + DangerousCircles.distance_to_another_dangerous_circle:
                return False
        return True

    def check_coords_other_dynamic_circles(self):
        # this method checks if the dangerous circle is as far as it needs from the other dangerous circles

        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            distance_to_other_dynamic_circle = sqrt((self.coords[0] - dynamic_circle.coords[0]) ** 2 + (
                        self.coords[1] - dynamic_circle.coords[1]) ** 2)
            if distance_to_other_dynamic_circle <= self.size + dynamic_circle.size + DynamicCircles.distance_to_another_dynamic_circle:
                return False
        return True

    def grow_dynamic_circle(self,radius):
        # this method counts how much the circle must grow
        # - radius - is the circle's radius

        dynamic_circle_area = Game.area_count(self.size)
        new_dynamic_circle_area = dynamic_circle_area + Game.area_count(radius)
        self.size = Game.radius_count(new_dynamic_circle_area)

    @staticmethod
    def check_grow_dynamic_circle():
        # this method checks if the dynamic circles don't eat something

        # this loop verifies if the circles didn't eat a static circle
        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            for static_circle in StaticCircles.static_circle_objects:
                distance_between_circles = sqrt((dynamic_circle.coords[0] - static_circle.coords[0])**2 + (dynamic_circle.coords[1] - static_circle.coords[1])**2)
                if distance_between_circles <= dynamic_circle.size:
                    dynamic_circle.grow_dynamic_circle(static_circle.size)
                    StaticCircles.static_circle_objects.remove(static_circle)

        # this loop verifies if the circles didn't eat another dynamic circle
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
        # this method checks if the dynamic circles don't touch a dangerous circle

        for dynamic_circle in DynamicCircles.dynamic_circle_objects:
            for dangerous_circle in DangerousCircles.dangerous_circle_objects:
                distance_between_circles = sqrt((dynamic_circle.coords[0] - dangerous_circle.coords[0]) ** 2 + (
                        dynamic_circle.coords[1] - dangerous_circle.coords[1]) ** 2)
                if distance_between_circles - (dynamic_circle.size + dangerous_circle.size) <= -DangerousCircles.dangerous_distance:
                            if dynamic_circle.size > Game.minimum_size:
                                dynamic_circle.size -= dynamic_circle.size * (dangerous_circle.lose_size / 100)
                                dynamic_circle.change_speed()
                            if dynamic_circle.size < Game.minimum_size:
                                 dynamic_circle.size = Game.minimum_size

    @staticmethod
    def draw_dynamic_circles():
        # this method draws all the static circles

        for circle in DynamicCircles.dynamic_circle_objects:
            pygame.draw.circle(DynamicCircles.window_surface,circle.color,circle.coords,circle.size)
        DynamicCircles.move_dynamic_circle()
        DynamicCircles.check_grow_dynamic_circle()
        DynamicCircles.check_dangerous_circles()

    @staticmethod
    def generate_all_possible_speed():
        # this method only generates all the possible speeds

        x = DynamicCircles.possible_speed[0]
        while x<=1:
            if (DynamicCircles.possible_speed[0] <= x <= DynamicCircles.possible_speed[1]) or (
                    DynamicCircles.possible_speed[2] <= x <= DynamicCircles.possible_speed[3]):
                DynamicCircles.interval_speed.append(x)
            x += 0.1

    @staticmethod
    def move_dynamic_circle():
        # this method moves the dynamic circles

        for circle in DynamicCircles.dynamic_circle_objects:
            circle.coords[0] += circle.speed[0]
            circle.coords[1] += circle.speed[1]
        DynamicCircles.verify_bound()

    @staticmethod
    def verify_bound():
        # this method verifies if the player's circle doesn't touch the borders. If it does it, it bounds

        for circle in DynamicCircles.dynamic_circle_objects:
            if circle.coords[0] + circle.size >= DynamicCircles.window_size[0] or circle.coords[0] - circle.size <= 0:
                circle.speed[0] = - circle.speed[0]
            if circle.coords[1] + circle.size >= DynamicCircles.window_size[1] or circle.coords[1] - circle.size <= 0:
                circle.speed[1] = - circle.speed[1]


    @staticmethod
    def delete_dynamic_circles():
        # this method checks if there aren't enough dynamic circles to start delete one by one

        if len(DynamicCircles.dynamic_circle_objects) >= DynamicCircles.min_nr_to_delete:
            DynamicCircles.dynamic_circle_objects.pop(randint(0,len(DynamicCircles.dynamic_circle_objects)-1))


    @staticmethod
    def choose_speed():
        # this method chooses a speed randomly

        return [DynamicCircles.interval_speed[randint(0, len(DynamicCircles.interval_speed) - 1)],
            DynamicCircles.interval_speed[randint(0, len(DynamicCircles.interval_speed) - 1)]]

    @staticmethod
    def choose_size():
        # this method chooses a size randomly

        return randint(DynamicCircles.initial_size[0], DynamicCircles.initial_size[1])

    @staticmethod
    def choose_color():
        # this method chooses a color randomly

        return DynamicCircles.color[randint(0, len(DynamicCircles.color) - 1)]

def start(window, window_size):

    # this method start the game
    # - window - is the window of the game
    # - __window_size - is the size of the window
    StaticCircles.window_size = window_size
    StaticCircles.window_surface = window.return_surface()
    DangerousCircles.window_size = window_size
    DangerousCircles.window_surface = window.return_surface()
    DynamicCircles.window_size = window_size
    DynamicCircles.window_surface = window.return_surface()
    game = Game(window, window_size)
    game.draw_game()
