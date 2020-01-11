import math
import random
import tkinter as tk
from PIL import Image, ImageTk

from game_window_components import ControlButtons, Score, ActMarble, MarbleCounter, NextMarble
from game_popupwindow import UsernamePopupWindow


class Window:
    playground_width = 660
    playground_height = 660
    bottom_toolbar_width = 650
    bottom_toolbar_height = 100
    right_toolbar_width = 150
    right_toolbar_height = 660
    border_width = 2
    color_background = '#047E97'

    def __init__(self):
        self.mouse_y = 0
        self.mouse_x = 0
        self.username = None  # username of current player
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
        self.root.title("Porygon")
        self.root.geometry("{}x{}".format(self.playground_width + self.right_toolbar_width,
                                          self.right_toolbar_height + self.bottom_toolbar_height))
        self.root.resizable(False, False)

        # create MAIN FRAME and set its properties
        self.main_frame = tk.Frame(self.root, bg=self.color_background)
        self.main_frame.pack(expand=True, fill='both')

        # create playground
        self.playground = tk.Canvas(self.main_frame,
                                    bg=self.color_background,
                                    width=self.playground_width - 2 * self.border_width,
                                    height=self.playground_height - 2 * self.border_width,
                                    relief='sunken',
                                    highlightthickness=self.border_width,
                                    highlightbackground="black")

        # create bottom toolbar
        self.bottom_toolbar = tk.Frame(self.main_frame,
                                       bg=self.color_background,
                                       width=self.bottom_toolbar_width,
                                       height=self.bottom_toolbar_height)

        # create right toolbar
        self.right_toolbar = tk.Frame(self.main_frame,
                                      bg=self.color_background,
                                      width=self.right_toolbar_width,
                                      height=self.right_toolbar_height)

        # create about frame in right bottom corner
        self.about_frame = tk.Frame(self.main_frame,
                                    bg=self.color_background,
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
                                     bg=self.color_background,
                                     font=("Helvetica", 16))

        # pack name of game and name of author to about frame
        self.name_of_game.grid(row=0, column=0)

        # prepare pictures
        self.init_pictures()

        # set background for playground
        self.background_image = None
        self.set_background()

        # prepare the marbles and place them in the playground
        self.init_marbles()
        self.show_marbles()
        # self.show_grid()

        # listeners for buttons action
        self.right_toolbar.restart_action = False

        self.control_buttons = ControlButtons(self.right_toolbar, self)
        self.score = Score(self.right_toolbar)

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
        self.you_won = True
        self.playground.fire_enabled = True
        self.seconds = 0
        self.achieved_score = 0

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

        # check whether you won (all marbles are grey)
        self.you_won = True
        for row in self.marbles:
            for marble in row:
                if marble != 7:
                    self.you_won = False
                    break

        if self.you_won:
            self.you_won = True

            # delete all marbles
            self.playground.delete('all')

            # set background back
            self.set_background()

            # starts animation
            self.winner_anim()

            # show popup windows for entering username
            self.username = UsernamePopupWindow(self.main_frame).show()
            if self.username == "":
                self.username = 'player'

            # find actual score and save it
            self.achieved_score = self.score.get_score()
            # print("Achieved Score:", self.achieved_score)
            self.control_buttons.save_highscore(self.username, self.achieved_score)

            # restart score
            self.score.restart_score()

            # initialization of new set of marbles
            self.marbles = self.init_marbles()
            self.show_marbles()
            # self.show_grid()

        # if there is marble in 13th row, game over
        for grey_ball in self.marbles[16]:
            if grey_ball != 7:
                print('Game Over')
                self.is_game_over = True
                break

        if self.is_game_over:
            self.is_game_over = False

            # delete all marbles
            self.playground.delete('all')

            # set background back
            self.set_background()

            # starts animation
            self.game_over_anim()

            # show popup windows for entering username
            self.username = UsernamePopupWindow(self.main_frame).show()
            if self.username == "":
                self.username = 'player'

            # find actual score and save it
            self.achieved_score = self.score.get_score()
            # print("Achieved Score:", self.achieved_score)
            self.control_buttons.save_highscore(self.username, self.achieved_score)

            # restart score
            self.score.restart_score()

            # initialization of new set of marbles
            self.marbles = self.init_marbles()
            self.show_marbles()
            # self.show_grid()

        if self.you_are_playing:
            self.playground.after(1000, self.timer)

    def fire_marble(self, event):
        """
        fires new marble, i.e. creates new object FiringMarble
        """
        # create new marble (only if there is no flying marble)
        if self.playground.fire_enabled:
            self.playground.fire_enabled = False

            self.firing_marble = FiringMarble(self.playground, event.x, event.y, self.act_marble.get_picture(),
                                              self.act_marble.get_color(), self.marbles, self)

            # set correct color to act marble
            self.update_act_marble_color()

            # update color of next marble
            self.update_next_marble_color()

    @staticmethod
    def init_marbles():
        """
        initialisation of marbles at the beginning of game
            rows = 5
            columns = 16
        """
        marbles = list()
        for row in range(7):
            marbles.append([])
            for column in range(16):
                # each marble has assigned random number form 1 to 6
                # numbers represent colors of marbles
                marbles[row].append(random.randint(1, 6))
                # marbles[row].append(7)
        for row in range(7, 17):
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
        self.playground.delete('all')
        self.set_background()
        x, y = self.border_width + 20, self.border_width + 20
        for i in range(len(self.marbles)):
            for j in range(len(self.marbles[i])):
                if self.marbles[i][j] != 7:  # don't show grey marbles
                    color = self.identify_color(self.marbles[i][j])
                    image = self.pictures[color]
                    self.playground.create_image(x, y, image=image)
                # self.playground.create_text(x, y - 10, text="{}:{}".format(x, y), font='Arial 7')
                # self.playground.create_text(x, y + 10, text="{}:{}".format(i, j), font='Arial 7')
                x += 40
            y += 40
            if i % 2 == 1:
                x = self.border_width + 20
            else:
                x = self.border_width + 20 + 20
        self.playground.update()

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
                # print("line")
                self.playground.create_line(x, y, x, y + 40)
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

    def game_over_anim(self):
        """
        show game-over animation at the end of game, it lasts cycles*len(array)*30 ms = 4*20*30 ms = 3 s
        """
        self.playground.fire_enabled = False
        cycles = 4
        array = []
        gif = Image.open('../images/game_over.gif')
        for i in range(gif.n_frames):
            gif.seek(i)
            array.append(ImageTk.PhotoImage(gif.resize((self.playground_width, self.playground_height))))

        tk_id = self.playground.create_image(self.border_width+self.playground_width//2,
                                             self.border_width+self.playground_height//2)
        i, j = 0, 0
        while j < cycles*len(array):
            self.playground.itemconfig(tk_id, image=array[i])
            i = (i + 1) % len(array)
            self.playground.update()
            self.playground.after(30)
            j += 1

        self.playground.fire_enabled = True

    def winner_anim(self):
        """
        show game-over animation at the end of game, it lasts cycles*len(array)*30 ms = 4*20*30 ms = 3 s
        """
        self.playground.fire_enabled = False
        cycles = 3
        array = []
        gif = Image.open('../images/winner.gif')
        for i in range(gif.n_frames):
            gif.seek(i)
            array.append(ImageTk.PhotoImage(gif.resize((self.playground_width, self.playground_height))))

        tk_id = self.playground.create_image(self.border_width+self.playground_width//2,
                                             self.border_width+self.playground_height//2)
        i, j = 0, 0
        while j < cycles*len(array):
            self.playground.itemconfig(tk_id, image=array[i])
            i = (i + 1) % len(array)
            self.playground.update()
            self.playground.after(100)
            j += 1

        self.playground.fire_enabled = True

    def set_background(self):
        """
        sets background for playground
        """
        name_of_picture = "../images/background.png"
        self.background_image = ImageTk.PhotoImage(Image.open(name_of_picture).resize((self.playground_width,
                                                                                       self.playground_height)))
        self.playground.create_image(self.border_width, self.border_width,
                                     image=self.background_image,
                                     anchor='nw')


class FiringMarble:
    init_x = 326.5
    init_y = 700
    speed = 4

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
        self.neighb_with_same_color = 0
        self.list_of_erased_marbles = set()
        self.list_of_disconnected_marbles = set()

        # set x and y
        self.x = self.init_x
        self.y = self.init_y

        # set row and column
        self.row = 100
        self.column = 100

        # set previous row and column
        self.prev_row, self.prev_column = 12, 6

        # where to fall?
        self.where_to_fall = None
        self.speed = 2

        # calculate dx and dy
        # fi is angle to which I shoot (event when marble is bounced from right/left mantinel, fi is same)
        self.fi = math.atan(abs((self.direction_y - self.init_y) / (self.direction_x - self.init_x)))
        self.dy = -4 * math.sin(self.fi)
        # print("First FI =", math.degrees(self.fi))

        if self.direction_x < self.init_x:
            self.dx = -4 * math.cos(self.fi)
        else:
            self.dx = 4 * math.cos(self.fi)

        # immediately it must start moving
        self.inner_timer()

    def inner_timer(self):
        """
        inner timer for flying marble
        it stops when you touch another marble of mantinel
        """
        if self.something_touched_me:

            # print("I touched something")
            # print("ROW:COLUMN =", self.row, self.column)
            # print("FI:", self.fi*180/math.pi)

            # print("Where to fall:", self.where_to_fall)
            x_targ, y_targ = self.middle_of_cell(self.where_to_fall)
            self.fi = math.atan(abs((y_targ - self.y) / (x_targ - self.x)))
            self.speed = 1
            # print("FI:", self.fi*180/math.pi)

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
        """
        starts second timer when a marble knows where to fall, it leads marble to that position
        """

        if self.me_in_middle:
            # add the marble to array of marbles at the right position
            self.marbles[self.where_to_fall[0]][self.where_to_fall[1]] = self.color
            # print("Where to fall:", self.where_to_fall)

            # print actual marbles
            # for row in self.marbles:
            #     print(row)

            # enabled firing another marble
            self.playground.fire_enabled = True

            # recursively destroy all marbles that have same color and are connected to through same-color marble
            self.find_same_color_marbles(self.where_to_fall[0], self.where_to_fall[1], self.color)

            # do sth
            # print("DEBUG:", self.neighb_with_same_color)
            if self.neighb_with_same_color >= 3:
                # add me to the list
                self.list_of_erased_marbles.add((self.where_to_fall[0], self.where_to_fall[1]))
                # print list of to-be erased marbles
                # print("To- be erased marbles:", self.list_of_erased_marbles)
                # find score
                self.neighb_with_same_color = len(self.list_of_erased_marbles)
                # destroy them !!!
                # print("# of neighbours with same color:", self.neighb_with_same_color)
                self.destroy_neighbours()
            else:
                # remove one marble from next_marble_counter
                number = self.window.next_marble_counter.get_counter()
                self.window.next_marble_counter.set_number_of_marbles(number-1)

            # add random rows when next marble counter hits 0
            if self.window.next_marble_counter.get_counter() == 0:
                self.marbles.insert(0, self.random_row())
                # set new counter fo next marble (random number from 2 to 5)
                self.window.next_marble_counter.set_number_of_marbles(random.randint(2, 5))

            # add the number of erased marbles to actual score
            if self.neighb_with_same_color >= 3:
                # print("Add to score:", self.neighb_with_same_color**2)
                self.window.score.add_to_score(self.neighb_with_same_color**2)

            # reset counter for neighbours with same color
            self.neighb_with_same_color = 0
            self.list_of_erased_marbles = set()

            # hide myself
            self.playground.itemconfigure(self.marble, state='hidden')

            # # print current marbles
            # print("show marbles:\n")
            # for line in self.marbles:
            #     for number in line:
            #         if number != 7:
            #             print(number, end=' ')
            #         else:
            #             print('.', end=' ')
            #     print()

            # update playground with erased marbles
            self.window.show_marbles()
            # self.window.show_grid()

            self.list_of_disconnected_marbles = set()   # contains tuples (row, column) of marbles
            self.find_disconnected_marbles()            # finds disconnected marbles

            if len(self.list_of_disconnected_marbles) > 0:
                # add 10 points to score for each single marble
                # print("Add to score:", 10*len(self.list_of_disconnected_marbles))
                self.window.score.add_to_score(10*len(self.list_of_disconnected_marbles))

                self.destroy_disconnected()             # erases disconnected marbles

            # reset list of disconnected marbles
            self.list_of_disconnected_marbles = set()

            # update playground with erased disconnected marbles
            self.window.show_marbles()
            # self.window.show_grid()

        else:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.playground.coords(self.marble, self.x, self.y)

            self.playground.after(self.speed, self.second_inner_timer)

            # check whether I am in middle
            self.me_in_middle = self.is_close()

    @staticmethod
    def random_row():
        """
        generates randomly colored row that is added at the top
        """
        row = []
        for column in range(16):
            # each marble has assigned random number form 1 to 6
            # numbers represent colors of marbles
            row.append(random.randint(1, 6))

        return row

    def touched_or_mantinel(self):
        """
        tells me when to stop
        """
        # detect cell to which the marble currently belong
        self.row, self.column = self.detect_cell()

        # i have got an array of marbles that are currently on playground: self.marbles
        # check whether I hit right or left mantinel
        if self.x - 21 < 0 or self.x + 21 >= Window.playground_width:
            self.dx *= -1  # change direction in x axis
        elif self.y - 21 < 0:  # Am I at the top mantinel??? Then stop!
            return True

        # check for marble in my way anyway
        if self.marble_in_my_way():
            # print("Marble in my way. I am at the: {}:{}".format(self.row, self.column))
            return True

        # otherwise I didn't touch anything
        return False

    def detect_cell(self):
        """
        detects row and column of current cell
        """
        row = int((self.y - Window.border_width) // 40)

        if row % 2 == 0:  # starts on the left mantinel
            column = int((self.x - Window.border_width) // 40)
        else:
            column = int((self.x - Window.border_width - 20) // 40)

        # don't jump of the grid
        if column >= 16:
            column = 15
        if column < 0:
            column = 0

        return row, column

    @staticmethod
    def middle_of_cell(coords):
        """
        returns coordinates of given cell
        """
        row, column = coords[0], coords[1]

        y = Window.border_width + 40 * row + 20

        if row % 2 == 0:  # starts on the left mantinel
            x = Window.border_width + 40 * column + 20
        else:  # starts 20 pixel away from the right mantinel
            x = Window.border_width + 40 * column + 20 + 20
        return x, y

    def is_close(self):
        """
        return True if marble is close to the middle of target cell
        """
        x, y = self.middle_of_cell(self.where_to_fall)

        dist = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

        return dist < 1

    def marble_in_my_way(self):
        """
        tells mi where to fall when something is in my way
        """

        # I have: fi, row, column, marbles
        # print("In marble_in_my_way:", self.row, self.column)

        # I am at the left mantinel
        if self.column == 0 and self.dx < 0:
            # print("I am at the left mantinel")
            if self.marbles[self.row-1][self.column] != 7:
                self.where_to_fall = (self.row, self.column)
                return True

        # I am at the right mantinel
        elif self.column == len(self.marbles[0])-1 and self.dx > 0:
            # print("I am at the right mantinel")
            if self.marbles[self.row-1][self.column] != 7:
                self.where_to_fall = (self.row, self.column)
                return True

        # I am at the top mantinel
        elif self.row == 0:
            # print("I am at the top mantinel")
            self.where_to_fall = (self.row, self.column)
            return True

        # I am somewhere inside
        elif self.row % 2 == 0:  # starts on the left mantinel
            # print("row % 2 = 0")

            # to the right, 0 < fi < pi/6 - ok
            if 0 < self.fi < math.pi / 6 and self.dx > 0:
                # print("to the right, 0 < fi < pi/6")
                try:
                    if self.marbles[self.row][self.column + 1] != 7:

                        if self.marbles[self.row - 1][self.column] == 7:
                            self.where_to_fall = (self.row - 1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column - 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                    else:
                        if self.marbles[self.row - 1][self.column + 1] != 7:
                            self.where_to_fall = (self.row, self.column + 1)
                            return True

                except IndexError:
                    print("IndexError")

            # to the right: pi/6 < fi < pi/3
            elif math.pi / 6 < self.fi <= math.pi / 3 and self.dx > 0:
                # print("to the right: pi/6 < fi < pi/3")
                try:
                    if self.marbles[self.row - 1][self.column] != 7:
                        if self.marbles[self.row][self.column + 1] == 7:
                            self.where_to_fall = (self.row, self.column + 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column + 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True

                except IndexError:
                    print("IndexError")

            # to the right: pi/3 < fi < pi/2
            elif math.pi / 3 < self.fi <= math.pi / 2 and self.dx > 0:
                # print("to the right: pi/3 < fi < pi/2")
                try:
                    if self.marbles[self.row - 1][self.column] != 7:
                        if self.marbles[self.row - 1][self.column - 1] == 7:
                            self.where_to_fall = (self.row - 1, self.column - 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column - 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

            # to the left, 0 < fi < pi/6 - ok
            if 0 < self.fi < math.pi / 6 and self.dx < 0:
                # print("to the left, 0 < fi < pi/6")
                try:
                    if self.marbles[self.row][self.column - 1] != 7:
                        if self.marbles[self.row - 1][self.column - 1] == 7:
                            self.where_to_fall = (self.row - 1, self.column - 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column + 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                    else:
                        if self.marbles[self.row - 1][self.column - 2] != 7:
                            self.where_to_fall = (self.row, self.column - 1)
                            return True

                except IndexError:
                    print("IndexError")

            # to the left: pi/6 < fi < pi/3
            elif math.pi / 6 < self.fi <= math.pi / 3 and self.dx < 0:
                # print("to the left: pi/6 < fi < pi/3")
                try:
                    if self.marbles[self.row - 1][self.column - 1] != 7:
                        if self.marbles[self.row][self.column - 1] == 7:
                            self.where_to_fall = (self.row, self.column - 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

            # to the left: pi/3 < fi < pi/2
            elif math.pi / 3 < self.fi <= math.pi / 2 and self.dx < 0:
                # print("to the left: pi/3 < fi < pi/2")
                try:
                    if self.marbles[self.row - 1][self.column - 1] != 7:
                        if self.marbles[self.row - 1][self.column] == 7:
                            self.where_to_fall = (self.row - 1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

        elif self.row % 2 == 1:  # starts 20 pixel away from the right mantinel
            # print("row % 2 = 1")

            # to the right, 0 < fi < pi/6
            if 0 < self.fi < math.pi / 6 and self.dx > 0:
                # print("to the right, 0 < fi < pi/6")
                try:
                    if self.marbles[self.row][self.column + 1] != 7:
                        if self.marbles[self.row - 1][self.column + 1] == 7:
                            self.where_to_fall = (self.row - 1, self.column + 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column - 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                    else:
                        if self.marbles[self.row - 1][self.column + 2] != 7:
                            self.where_to_fall = (self.row, self.column + 1)
                            return True

                except IndexError:
                    print("IndexError")

            # to the right: pi/6 < fi < pi/3
            elif math.pi / 6 < self.fi <= math.pi / 3 and self.dx > 0:
                # print("to the right: pi/6 < fi < pi/3")
                try:
                    if self.marbles[self.row - 1][self.column + 1] != 7:
                        if self.marbles[self.row][self.column + 1] == 7:
                            self.where_to_fall = (self.row, self.column + 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

            # to the right: pi/3 < fi < pi/2
            elif math.pi / 3 < self.fi <= math.pi / 2 and self.dx > 0:
                # print("to the right: pi/3 < fi < pi/2")
                try:
                    if self.marbles[self.row - 1][self.column + 1] != 7:
                        if self.marbles[self.row - 1][self.column] == 7:
                            self.where_to_fall = (self.row - 1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

            # to the left, 0 < fi < pi/6 - ok
            if 0 < self.fi < math.pi / 6 and self.dx < 0:
                # print("to the left, 0 < fi < pi/6")
                try:
                    if self.marbles[self.row][self.column - 1] != 7:
                        if self.marbles[self.row - 1][self.column] == 7:
                            self.where_to_fall = (self.row - 1, self.column)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row, self.column + 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                    else:
                        if self.marbles[self.row - 1][self.column - 1] != 7:
                            self.where_to_fall = (self.row, self.column - 1)
                            return True

                except IndexError:
                    print("IndexError")

            # to the left: pi/6 < fi < pi/3
            elif math.pi / 6 < self.fi <= math.pi / 3 and self.dx < 0:
                # print("to the left: pi/6 < fi < pi/3")
                try:
                    if self.marbles[self.row - 1][self.column] != 7:
                        if self.marbles[self.row][self.column - 1] == 7:
                            self.where_to_fall = (self.row, self.column - 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column + 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

            # to the left: pi/3 < fi < pi/2
            elif math.pi / 3 < self.fi <= math.pi / 2 and self.dx < 0:
                # print("to the left: pi/3 < fi < pi/2")
                try:
                    if self.marbles[self.row - 1][self.column] != 7:
                        if self.marbles[self.row - 1][self.column + 1] == 7:
                            self.where_to_fall = (self.row - 1, self.column + 1)
                        else:
                            if self.marbles[self.row][self.column] != 7:
                                self.where_to_fall = (self.row + 1, self.column + 1)
                            else:
                                self.where_to_fall = (self.row, self.column)
                        return True
                except IndexError:
                    print("IndexError")

        return False

    def find_same_color_marbles(self, row, column, my_color):
        """
        finds marbles that have same color as me and are connected to me
        """
        # I have self.color, self.where_to_fall and self.marbles
        # go through my neighbours and destroy them if they have same color and call this function again

        # print("starting to finding same color neighbours:", my_color)
        # set correct neighbours
        if row == 0 and (column != 0 and column != len(self.marbles[0])-1):
            neighbours = [(row, column + 1), (row, column - 1), (row + 1, column - 1), (row + 1, column)]
        elif row == 0 and column == 0:
            neighbours = [(row, column + 1), (row + 1, column)]
        elif row == 0 and column == len(self.marbles[0])-1:
            neighbours = [(row, column - 1), (row + 1, column - 1), (row + 1, column)]

        elif column == 0 and row % 2 == 0:
            neighbours = [(row, column + 1), (row - 1, column), (row + 1, column)]
        elif column == 0 and row % 2 == 1:
            neighbours = [(row, column + 1), (row - 1, column + 1), (row - 1, column), (row + 1, column),
                          (row + 1, column + 1)]

        elif column == len(self.marbles[0])-1 and row % 2 == 0:
            neighbours = [(row - 1, column), (row - 1, column - 1), (row, column - 1), (row + 1, column - 1),
                          (row + 1, column)]
        elif column == len(self.marbles[0])-1 and row % 2 == 1:
            neighbours = [(row - 1, column), (row, column - 1), (row + 1, column)]

        else:
            if row % 2 == 0:
                neighbours = [(row, column + 1), (row - 1, column), (row - 1, column - 1),
                              (row, column - 1), (row + 1, column - 1), (row + 1, column)]
            else:
                neighbours = [(row, column + 1), (row - 1, column + 1), (row - 1, column),
                              (row, column - 1), (row + 1, column), (row + 1, column + 1)]

        # print("\nYou are at [{}:{}]".format(row, column))
        # print("These are your neighbours:", neighbours)

        # check all neighbours and if one has same color as I have, remember it
        coords_with_same_color = []
        for coords in neighbours:
            ii = coords[0]
            jj = coords[1]

            if self.marbles[ii][jj] == my_color:
                coords_with_same_color.append((ii, jj))

        # print("same color neighbours:", coords_with_same_color)

        # call this function again for those neighbours that have same color
        if len(coords_with_same_color) != 0:
            for coords in coords_with_same_color:
                ii = coords[0]
                jj = coords[1]

                if (ii, jj) not in self.list_of_erased_marbles:
                    self.list_of_erased_marbles.add((ii, jj))
                    self.find_same_color_marbles(ii, jj, self.marbles[ii][jj])
                    self.neighb_with_same_color += 1
        else:
            # print("trivial case")
            pass

    def destroy_neighbours(self):
        """
        destroys every marble in self.list_of_erased_marbles
        """
        # print("erasing these marbles:", end=' ')
        for coords in self.list_of_erased_marbles:
            ii = coords[0]
            jj = coords[1]
            # print(coords, end=' ')
            self.marbles[ii][jj] = 7
        # print()

    def find_disconnected_marbles(self):
        """
        finds marbles that are not connected to to top mantinel and are alone
        (only works for one marble being alone)
        """
        for row in range(1, len(self.marbles)-1):
            for column in range(len(self.marbles[0])):
                if self.marbles[row][column] != 7:

                    # set correct neighbours
                    if row == 0 and (column != 0 and column != len(self.marbles[0])-1):
                        neighbours = [(row, column + 1), (row, column - 1), (row + 1, column - 1), (row + 1, column)]
                    elif row == 0 and column == 0:
                        neighbours = [(row, column + 1), (row + 1, column)]
                    elif row == 0 and column == len(self.marbles[0])-1:
                        neighbours = [(row, column - 1), (row + 1, column - 1), (row + 1, column)]

                    elif column == 0 and row % 2 == 0:
                        neighbours = [(row, column + 1), (row - 1, column), (row + 1, column)]
                    elif column == 0 and row % 2 == 1:
                        neighbours = [(row, column + 1), (row - 1, column + 1), (row - 1, column), (row + 1, column),
                                      (row + 1, column + 1)]

                    elif column == len(self.marbles[0])-1 and row % 2 == 0:
                        neighbours = [(row - 1, column), (row - 1, column - 1), (row, column - 1),
                                      (row + 1, column - 1), (row + 1, column)]
                    elif column == len(self.marbles[0])-1 and row % 2 == 1:
                        neighbours = [(row - 1, column), (row, column - 1), (row + 1, column)]

                    else:
                        if row % 2 == 0:
                            neighbours = [(row, column + 1), (row - 1, column), (row - 1, column - 1),
                                          (row, column - 1), (row + 1, column - 1), (row + 1, column)]
                        else:
                            neighbours = [(row, column + 1), (row - 1, column + 1), (row - 1, column),
                                          (row, column - 1), (row + 1, column), (row + 1, column + 1)]

                    # check these neighbours

                    is_alone = True
                    for coords in neighbours:
                        ii = coords[0]
                        jj = coords[1]
                        # print("Looking at:", ii, jj)

                        if self.marbles[ii][jj] != 7:
                            # print("is not 7")
                            is_alone = False

                    if is_alone:
                        self.list_of_disconnected_marbles.add((row, column))

    def destroy_disconnected(self):
        """
        destroys every marble in self.list_of_disconnected_marbles
        """
        # print("erasing these marbles:", end=' ')
        for coords in self.list_of_disconnected_marbles:
            ii = coords[0]
            jj = coords[1]
            # print(coords, end=' ')
            self.marbles[ii][jj] = 7
        # print()
