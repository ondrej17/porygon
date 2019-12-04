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

        self.name_of_author = tk.Label(self.about_frame,
                                       text='Ondrej Bily',
                                       bg='#C0C0FF',
                                       font=("Helvetica", 12))

        # pack name of game and name of author to about frame
        self.name_of_author.pack()
        self.name_of_game.pack()

        # prepare pictures
        self.init_pictures()

        # prepare the marbles and place them in the playground
        self.init_marbles()
        #self.show_marbles()

        # TODO: add functionality to the buttons and make the the score counter work
        self.control_buttons = ControlButtons(self.right_toolbar)
        self.score = Score(self.right_toolbar)

        # TODO: add canon, next marbles to the playground
        # set color of actual and next marble randomly
        self.next_marble = NextMarble(self.bottom_toolbar, self.pictures[self.color_map[random.randint(1, 6)]])
        self.next_marble_counter = MarbleCounter(self.bottom_toolbar, self.pictures[self.color_map[7]])
        self.act_marble = ActMarble(self.bottom_toolbar, self.pictures[self.color_map[random.randint(1, 6)]])

        # bind button1 click to fire function
        self.playground.bind('<Button-1>', self.fire_marble)
        self.you_are_playing = True

        # start the timer
        self.timer()

        # at the end of __init__
        self.root.mainloop()

    def timer(self):
        print('tik')
        if self.you_are_playing:
            self.playground.after(1000, self.timer)

    def fire_marble(self, event):
        #print('Mouse clicked at:', event.x, event.y)

        # create new marble
        self.firing_marble = FiringMarble(self.playground, event.x, event.y, self.act_marble.get_picture(), self.marbles)

        # set correct color to act marble
        self.update_act_marble_color()

        # update color of next marble
        self.update_next_marble_color()

    def init_marbles(self):
        """
        initialisation of marbles at the beginning of game
        """
        marbles = list()
        for row in range(7):
            marbles.append([])
            for column in range(16):
                # each marble has assigned random number form 1 to 6
                # numbers represent colors of marbles
                marbles[row].append(random.randint(1, 6))
        for row in range(7, 12):
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
                color = self.identify_color(self.marbles[i][j])
                image = self.pictures[color]
                self.playground.create_image(x, y, image=image)
                x += 39
            y += 39
            if i % 2 == 1:
                x = self.border_width + 20
            else:
                x = self.border_width + 20 + 19.5

    def init_pictures(self):
        """
        creates a dictionary self.pictures: [color] [picture]
        """
        for color in self.color_map.values():
            name_of_picture = "../images/marble_{}.png".format(color)
            img = Image.open(name_of_picture).resize((40, 40), Image.ANTIALIAS)
            self.pictures[color] = ImageTk.PhotoImage(img)

    def update_next_marble_color(self):
        self.next_marble.update_color(self.pictures[self.color_map[random.randint(1, 6)]])

    def update_act_marble_color(self):
        next_color = self.next_marble.get_color()
        self.act_marble.update_color(next_color)


class FiringMarble:
    init_x = 326.5
    init_y = 550

    # TODO: speed must be adjust for each direction
    speed = 5

    def __init__(self, playground, dir_x, dir_y, picture, marbles):
        # this is the direction of fired marble
        self.marbles = marbles  # it adds itself to this array at the end
        self.direction_x = dir_x
        self.direction_y = dir_y
        self.playground = playground
        self.picture = picture

        self.marble = self.playground.create_image(self.init_x, self.init_y,
                                                   image=self.picture)
        self.something_touched_me = False

        #print('Direction:', self.direction_x, self.direction_y)
        #print('Initial:  ', self.init_x, self.init_y)
        # set x and y
        self.x = self.init_x
        self.y = self.init_y

        # find dx and dy
        if self.direction_x < self.init_x:
            self.dx = -2
        else:
            self.dx = 2
        self.dy = self.dx*(self.direction_y - self.init_y)/(self.direction_x - self.init_x)

        # immediately it must start moving
        self.inner_timer()

    def inner_timer(self):
        #print('Position:', self.x, self.y)
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.playground.coords(self.marble, self.x, self.y)

        if not self.something_touched_me:
            self.playground.after(self.speed, self.inner_timer)

            # check if something touched me
            self.something_touched_me = self.touched_or_mantinel()

        if self.something_touched_me:
            print("I arrived at the borders")
            # TODO: add the marble to array of marbles at the right position
            #self.marbles[correct_position][correct_position] = self.picture

    def touched_or_mantinel(self):
        if self.x - 21 < 0 or self.x + 21 >= Window.playground_width:
            self.dx *= -1
        elif self.y - 21 < 0:   # TODO: marbles stops after top mantinel (depends on direction)
            return True

        return False



