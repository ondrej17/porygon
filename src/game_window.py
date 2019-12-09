import math
import random
import tkinter as tk
from PIL import Image, ImageTk

from game_window_components import ControlButtons, Score, ActMarble, MarbleCounter, NextMarble


class Window:
    playground_width = 650
    playground_height = 500
    bottom_toolbar_width = 650
    bottom_toolbar_height = 100
    right_toolbar_width = 150
    right_toolbar_height = 500
    border_width = 2

    def __init__(self, username):
        self.mouse_y = 0
        self.mouse_x = 0
        self.username = username  # username of current player
        self.marbles = self.init_marbles()  # set of all marbles at the beginning of game
        self.color_map = {  # dictionary for resolving color from number
            1: 'blue',
            2: 'blue_dark',
            3: 'green',
            4: 'purple',
            5: 'red',
            6: 'yellow',
            7: 'grey'
        }
        self.pictures = {}  # set of all tk.PhotoImage objects that are used for marbles
        self.firing_marble = None

        # create Tk() object and set its properties
        self.root = tk.Tk()
        self.root.title("Porygon - {}".format(username))
        self.root.geometry("{}x{}".format(self.playground_width + self.right_toolbar_width,
                                          self.right_toolbar_height + self.bottom_toolbar_height))
        self.root.resizable(False, False)

        # create MAIN FRAME and set its properties
        self.main_frame = tk.Frame(self.root, bg='#C0C0FF')
        self.main_frame.pack(expand=True, fill='both')

        # create playground
        self.playground = tk.Canvas(self.main_frame,
                                    bg='#C0C0FF',
                                    width=self.playground_width - 2 * self.border_width,
                                    height=self.playground_height - 2 * self.border_width,
                                    relief='sunken',
                                    borderwidth=self.border_width)

        # create bottom toolbar
        self.bottom_toolbar = tk.Frame(self.main_frame,
                                       bg='#C0C0FF',
                                       width=self.bottom_toolbar_width,
                                       height=self.bottom_toolbar_height)

        # create right toolbar
        self.right_toolbar = tk.Frame(self.main_frame,
                                      bg='#C0C0FF',
                                      width=self.right_toolbar_width,
                                      height=self.right_toolbar_height)

        # create about frame in right bottom corner
        self.about_frame = tk.Label(self.main_frame,
                                    bg='#C0C0FF',
                                    width=self.right_toolbar_width,
                                    height=self.bottom_toolbar_height)

        # set grid for playground, right toolbar, bottom toolbar and about frame
        self.playground.grid(row=0, column=0, padx=0, pady=0)
        self.right_toolbar.grid(row=0, column=1, padx=0, pady=0)
        self.bottom_toolbar.grid(row=1, column=0, padx=0, pady=0, sticky='w')
        self.about_frame.grid(row=1, column=1, padx=0, pady=0)

        # add information about game to about frame
        self.name_of_game = tk.Label(self.about_frame,
                                     text='Porygon',
                                     bg='#C0C0FF',
                                     font=("Helvetica", 16))

        # pack name of game and name of author to about frame
        self.name_of_game.pack()

        # prepare pictures
        self.init_pictures()

        # prepare the marbles and place them in the playground
        self.init_marbles()
        self.show_marbles()
        self.show_grid()

        # listeners for buttons action
        self.right_toolbar.restart_action = False

        # TODO: add functionality to the buttons and make the score counter work
        self.control_buttons = ControlButtons(self.right_toolbar)
        self.score = Score(self.right_toolbar)

        # TODO: add canon, next marbles to the playground
        # set color of actual and next marble randomly
        color = random.randint(1, 6)
        self.next_marble = NextMarble(self.bottom_toolbar, self.pictures[self.color_map[color]], color)
        self.next_marble_counter = MarbleCounter(self.bottom_toolbar, self.pictures[self.color_map[7]])
        color = random.randint(1, 6)
        self.act_marble = ActMarble(self.bottom_toolbar, self.pictures[self.color_map[color]], color)

        # bind button1 click to fire function
        self.playground.bind('<Button-1>', self.fire_marble)
        self.you_are_playing = True
        self.is_game_over = False
        self.playground.fire_enabled = True
        self.seconds = 0

        # start the timer
        self.timer()

        # at the end of __init__
        self.root.mainloop()

    def timer(self):
        # ticking clock
        # if self.seconds % 2 == 0:
        #     print('tik:', self.seconds)
        # else:
        #     print('tak:', self.seconds)
        self.seconds += 1

        # if there is marble in 13th row, game over
        for grey_ball in self.marbles[12]:
            if grey_ball != 7:
                print('Game Over')
                self.is_game_over = True

        # when Restart Button is clicked, restart_action is True and this happens
        if self.right_toolbar.restart_action or self.is_game_over:
            self.right_toolbar.restart_action = False
            self.is_game_over = False
            self.playground.delete('all')
            self.marbles = self.init_marbles()
            self.show_marbles()
            self.show_grid()

        if self.you_are_playing:
            self.playground.after(500, self.timer)

    def fire_marble(self, event):
        #print('Marble fired towards:', event.x, event.y)

        # create new marble (only if there is no flying marble)
        if self.playground.fire_enabled:
            self.playground.fire_enabled = False

            self.firing_marble = FiringMarble(self.playground, event.x, event.y, self.act_marble.get_picture(),
                                              self.act_marble.get_color(), self.marbles, self)

            # set correct color to act marble
            self.update_act_marble_color()

            # update color of next marble
            self.update_next_marble_color()

    def init_marbles(self):
        """
        initialisation of marbles at the beginning of game
        """
        marbles = list()
        for row in range(6):
            marbles.append([])
            for column in range(16):
                # each marble has assigned random number form 1 to 6
                # numbers represent colors of marbles
                marbles[row].append(random.randint(1, 6))
                # marbles[row].append(7)
        for row in range(6, 16):
            marbles.append([])
            for column in range(16):
                # each marble has assigned random number form 1 to 6
                # numbers represent colors of marbles
                marbles[row].append(7)

        return marbles

    def identify_color(self, number):
        """
        identifies color from given number based on color_map
        """
        return self.color_map[number]

    def show_marbles(self):
        """
        shows marbles in playground
        """
        x, y = self.border_width + 20, self.border_width + 20
        for i in range(len(self.marbles)):
            for j in range(len(self.marbles[i])):
                if self.marbles[i][j] != 7:     # don't show grey marbles
                    color = self.identify_color(self.marbles[i][j])
                    image = self.pictures[color]
                    self.playground.create_image(x, y, image=image)
                self.playground.create_text(x, y-10, text="{}:{}".format(x, y), font='Arial 7')
                self.playground.create_text(x, y+10, text="{}:{}".format(i, j), font='Arial 7')
                x += 40
            y += 40
            if i % 2 == 1:
                x = self.border_width + 20
            else:
                x = self.border_width + 20 + 20

    def show_grid(self):
        """
        shows grid in playground
        """
        y = 2

        for j in range(len(self.marbles)):
            if j % 2 == 1:
                x = self.border_width + 20
            else:
                x = self.border_width + 20 + 20

            for i in range(len(self.marbles[j])):
                #print("line")
                self.playground.create_line(x, y, x, y+40)
                x += 40
            self.playground.create_line(2, y, 646, y)
            y += 40

    def init_pictures(self):
        """
        creates a dictionary self.pictures: [color] [picture]
        """
        for color in self.color_map.values():
            name_of_picture = "../images/marble_{}.png".format(color)
            img = Image.open(name_of_picture).resize((40, 40), Image.ANTIALIAS)
            self.pictures[color] = ImageTk.PhotoImage(img)

    def update_next_marble_color(self):
        """
        updates color of next marble to random color
        """
        color = random.randint(1, 6)
        self.next_marble.update_color(self.pictures[self.color_map[color]], color)

    def update_act_marble_color(self):
        """
        updates color of act marble based on the color of next marble
        """
        next_color = self.next_marble.get_picture()
        self.act_marble.update_color(next_color, self.next_marble.get_color())


class FiringMarble:
    init_x = 326.5
    init_y = 550
    speed = 10

    def __init__(self, playground, dir_x, dir_y, picture, color, marbles, window):
        # this is the direction of fired marble
        self.marbles = marbles  # it adds itself to this array at the end
        self.direction_x = dir_x
        self.direction_y = dir_y
        self.playground = playground
        self.picture = picture
        self.color = color
        self.window = window

        self.marble = self.playground.create_image(self.init_x, self.init_y,
                                                   image=self.picture)
        self.something_touched_me = False
        self.second_timer_first_time = True
        self.me_in_middle = False

        # set x and y
        self.x = self.init_x
        self.y = self.init_y

        # set row and column
        self.row = 100
        self.column = 100

        # where to fall?
        self.where_to_fall = (-1, -1)
        self.speed = 5

        # calculate dx and dy
        # fi is angle to which I shoot (event when marble is bounced from right/left mantinel, fi is same)
        self.fi = math.atan(abs((self.direction_y - self.init_y)/(self.direction_x - self.init_x)))
        self.dy = -5*math.sin(self.fi)
        print("First FI =", math.degrees(self.fi))

        if self.direction_x < self.init_x:
            self.dx = -5*math.cos(self.fi)
        else:
            self.dx = 5*math.cos(self.fi)

        # immediately it must start moving
        self.inner_timer()

    def inner_timer(self):
        """
        inner timer for flying marble
        it stops when you touch another marble of mantinel
        """
        if self.something_touched_me:

            print("I touched something")
            print("ROW:COLUMN =", self.row, self.column)

            x_targ, y_targ = self.middle_of_cell(self.where_to_fall)
            self.fi = math.atan(abs((y_targ - self.y)/(x_targ - self.x)))
            self.speed = 10

            if y_targ < self.y and x_targ < self.x:
                self.dy = -math.sin(self.fi)
                self.dx = -math.cos(self.fi)
            elif y_targ < self.y and x_targ > self.x:
                self.dy = -math.sin(self.fi)
                self.dx = math.cos(self.fi)
            elif y_targ > self.y and x_targ < self.x:
                self.dy = math.sin(self.fi)
                self.dx = -math.cos(self.fi)
            elif y_targ > self.y and x_targ > self.x:
                self.dy = math.sin(self.fi)
                self.dx = math.cos(self.fi)

            self.second_inner_timer()

        else:
            # print('Position:', self.x, self.y)
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.playground.coords(self.marble, self.x, self.y)

            self.playground.after(self.speed, self.inner_timer)

            # check if something touched me
            self.something_touched_me = self.touched_or_mantinel()

    def second_inner_timer(self):

        if self.me_in_middle:
            # add the marble to array of marbles at the right position
            self.marbles[self.where_to_fall[0]][self.where_to_fall[1]] = self.color

            # print actual marbles
            # for row in self.marbles:
            #     print(row)

            # enabled firing another marble
            self.playground.fire_enabled = True

            # hide myself
            self.playground.itemconfigure(self.marble, state='hidden')
            self.window.show_marbles()
        else:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.playground.coords(self.marble, self.x, self.y)

            self.playground.after(self.speed, self.second_inner_timer)

            # check whether I am in middle
            self.me_in_middle = self.is_close()

    def touched_or_mantinel(self):
        """
        tells me when to stop
        """

        # detect cell to which the marble currently belong
        self.row, self.column = self.detect_cell()

        # i have got an array of marbles that are currently on playground: self.marbles
        # check whether I hit right or left mantinel
        if self.x - 21 < 0 or self.x + 21 >= Window.playground_width:
            self.dx *= -1   # change direction in x axis
        elif self.y - 21 < 0:   # Am I at the top mantinel??? Then stop!
            return True
        elif self.marble_in_my_way():
            return True

        # otherwise I didn't touch anything
        return False

    def detect_cell(self):
        """
        detects row and column of current cell
        """
        row = (self.y - Window.border_width) // 40

        if row % 2 == 0:    # starts on the left mantinel
            column = (self.x - Window.border_width) // 40
        else:
            column = (self.x - Window.border_width - 20) // 40

        if column >= 16:
            column = 15

        return int(row), int(column)

    def middle_of_cell(self, coords):
        """
        returns coordinates of given cell
        """
        row, column = coords[0], coords[1]

        y = Window.border_width + 40 * row + 20

        if row % 2 == 0:   # starts on the left mantinel
            x = Window.border_width + 40 * column + 20
        else:                   # starts 20 pixel away from the right mantinel
            x = Window.border_width + 40 * column + 20 + 20
        return x, y

    def is_close(self):
        """
        return True if marble is close to the middle of target cell
        """
        x, y = self.middle_of_cell(self.where_to_fall)

        dist = math.sqrt((x-self.x)**2 + (y-self.y)**2)

        return dist < 1

    def marble_in_my_way(self):
        # TODO: periodic boundary condition appeared, remove it

        # I have: fi, row, column, marbles

        if self.row % 2 == 0:   # starts on the left mantinel

            # to the right, 0 < fi < pi/6
            if 0 < self.fi < math.pi/6 and self.dx > 0:
                try:
                    if self.marbles[self.row][self.column+1] != 7:
                        if self.marbles[self.row-1][self.column] == 7:
                            self.where_to_fall = (self.row-1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column-1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the right: pi/6 < fi < pi/3
            elif math.pi/6 < self.fi <= math.pi/3 and self.dx > 0:
                try:
                    if self.marbles[self.row-1][self.column] != 7:
                        if self.marbles[self.row][self.column+1] == 7:
                            self.where_to_fall = (self.row, self.column+1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the right: pi/3 < fi < pi/2
            elif math.pi/3 < self.fi <= math.pi/2 and self.dx > 0:
                try:
                    if self.marbles[self.row-1][self.column] != 7:
                        if self.marbles[self.row-1][self.column-1] == 7:
                            self.where_to_fall = (self.row-1, self.column-1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left, 0 < fi < pi/6
            if 0 < self.fi < math.pi/6 and self.dx < 0:
                try:
                    if self.marbles[self.row][self.column-1] != 7:
                        if self.marbles[self.row-1][self.column-1] == 7:
                            self.where_to_fall = (self.row-1, self.column-1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left: pi/6 < fi < pi/3
            elif math.pi/6 < self.fi <= math.pi/3 and self.dx < 0:
                try:
                    if self.marbles[self.row-1][self.column-1] != 7:
                        if self.marbles[self.row][self.column-1] == 7:
                            self.where_to_fall = (self.row, self.column-1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left: pi/3 < fi < pi/2
            elif math.pi/3 < self.fi <= math.pi/2 and self.dx < 0:
                try:
                    if self.marbles[self.row-1][self.column-1] != 7:
                        if self.marbles[self.row-1][self.column] == 7:
                            self.where_to_fall = (self.row-1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

        else:                   # starts 20 pixel away from the right mantinel

            # to the right, 0 < fi < pi/6
            if 0 < self.fi < math.pi/6 and self.dx > 0:
                try:
                    if self.marbles[self.row][self.column+1] != 7:
                        if self.marbles[self.row-1][self.column+1] == 7:
                            self.where_to_fall = (self.row-1, self.column+1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column-1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the right: pi/6 < fi < pi/3
            elif math.pi/6 < self.fi <= math.pi/3 and self.dx > 0:
                try:
                    if self.marbles[self.row-1][self.column+1] != 7:
                        if self.marbles[self.row][self.column+1] == 7:
                            self.where_to_fall = (self.row, self.column+1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the right: pi/3 < fi < pi/2
            elif math.pi/3 < self.fi <= math.pi/2 and self.dx > 0:
                try:
                    if self.marbles[self.row-1][self.column+1] != 7:
                        if self.marbles[self.row-1][self.column] == 7:
                            self.where_to_fall = (self.row-1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left, 0 < fi < pi/6
            if 0 < self.fi < math.pi/6 and self.dx < 0:
                try:
                    if self.marbles[self.row][self.column-1] != 7:
                        if self.marbles[self.row-1][self.column] == 7:
                            self.where_to_fall = (self.row-1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left: pi/6 < fi < pi/3
            elif math.pi/6 < self.fi <= math.pi/3 and self.dx < 0:
                try:
                    if self.marbles[self.row-1][self.column] != 7:
                        if self.marbles[self.row][self.column-1] == 7:
                            self.where_to_fall = (self.row, self.column-1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False

            # to the left: pi/3 < fi < pi/2
            elif math.pi/3 < self.fi <= math.pi/2 and self.dx < 0:
                try:
                    if self.marbles[self.row-1][self.column] != 7:
                        if self.marbles[self.row-1][self.column+1] == 7:
                            self.where_to_fall = (self.row-1, self.column+1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row+1, self.column+1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    return False




