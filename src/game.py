import random
import tkinter as tk
from PIL import Image, ImageTk


class Game:
    def __init__(self):
        # at the initialization create  window
        self.window = Window()

    # TODO: other methods for Game object


class Window:
    playground_width = 650
    playground_height = 500
    bottom_toolbar_width = 650
    bottom_toolbar_height = 100
    right_toolbar_width = 150
    right_toolbar_height = 500
    border_width = 2

    def __init__(self):
        self.marbles = self.init_marbles()
        self.name_of_game = None
        self.color_map = {
            1: 'blue',
            2: 'blue_dark',
            3: 'green',
            4: 'purple',
            5: 'red',
            6: 'yellow'
        }
        self.pictures = {}
        self.root = tk.Tk()
        self.root.title("Porygon")
        self.root.geometry("{}x{}".format(self.playground_width + self.right_toolbar_width,
                                          self.right_toolbar_height + self.bottom_toolbar_height))
        self.root.resizable(False, False)
        self.main_frame = tk.Frame(self.root, bg='#C0C0FF')
        self.main_frame.pack(expand=True)

        # create playground, bottom and right toolbar, and about-frame
        self.playground = tk.Canvas(self.main_frame,
                                    bg='#C0C0FF',
                                    width=self.playground_width - 2 * self.border_width,
                                    height=self.playground_height - 2 * self.border_width,
                                    relief='sunken',
                                    borderwidth=self.border_width)

        self.bottom_toolbar = tk.Frame(self.main_frame,
                                       bg='#C0C0FF',
                                       width=self.bottom_toolbar_width,
                                       height=self.bottom_toolbar_height)

        self.right_toolbar = tk.Frame(self.main_frame,
                                      bg='#C0C0FF',
                                      width=self.right_toolbar_width,
                                      height=self.right_toolbar_height)

        self.about_frame = tk.Label(self.main_frame,
                                    bg='#C0C0FF',
                                    width=self.right_toolbar_width,
                                    height=self.bottom_toolbar_height)

        # pack playground and right frame to main_frame
        self.playground.grid(row=0, column=0, padx=0, pady=0)
        self.right_toolbar.grid(row=0, column=1, padx=0, pady=0)
        self.bottom_toolbar.grid(row=1, column=0, padx=0, pady=0)
        self.about_frame.grid(row=1, column=1, padx=0, pady=0)

        # add Porygon and Ondrej Bily to about-frame
        self.name_of_game = tk.Label(self.about_frame,
                                     text='Porygon',
                                     bg='#C0C0FF',
                                     font=("Helvetica", 16))

        self.name_of_author = tk.Label(self.about_frame,
                                       text='Ondrej Bily',
                                       bg='#C0C0FF',
                                       font=("Helvetica", 12))

        self.name_of_author.pack()
        self.name_of_game.pack()

        # prepare the marbles and place them in the playground
        self.init_pictures()
        self.init_marbles()
        self.show_marbles()

        # TODO: add stuff to the right frame
        self.score = Score(self.right_toolbar)
        self.control_buttons = ControlButtons(self.right_toolbar)

        # TODO: add canon, next marbles to the playground
        self.act_marble = ActMarble(self.bottom_toolbar)
        self.next_marble_counter = MarbleCounter(self.bottom_toolbar)
        self.next_marble_color = NextMarble(self.bottom_toolbar)

        # at the end of __init__
        self.root.mainloop()

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


class ControlButtons:
    def __init__(self, frame):
        # width of buttons must be together equal to right_toolbar_width from Window
        # TODO: create png images for these buttons, they may have different size, color
        #  and they must have a name on itself restart button

        # restart button
        img = Image.open('../images/marble_green_restart.png').resize((70, 70), Image.ANTIALIAS)
        self.restart_btn_image = ImageTk.PhotoImage(img)
        restart_btn = tk.Button(frame, width=75,
                                image=self.restart_btn_image,
                                bg='#C0C0FF',
                                relief='flat',
                                command=self.click_restart,
                                borderwidth=0,
                                activebackground='#C0C0FF')
        restart_btn.grid(row=0, column=0)

        # help button
        img = Image.open('../images/marble_purple_help.png').resize((50, 50), Image.ANTIALIAS)
        self.help_btn_image = ImageTk.PhotoImage(img)

        restart_btn = tk.Button(frame, width=75,
                                image=self.help_btn_image,
                                bg='#C0C0FF',
                                relief='flat',
                                command=self.click_help,
                                borderwidth=0,
                                activebackground='#C0C0FF')
        restart_btn.grid(row=1, column=1)

        # high-score button
        img = Image.open('../images/marble_red_highscore.png').resize((80, 80), Image.ANTIALIAS)
        self.highscore_btn_image = ImageTk.PhotoImage(img)

        highscore_btn = tk.Button(frame, width=75,
                                  image=self.highscore_btn_image,
                                  bg='#C0C0FF',
                                  relief='flat',
                                  command=self.click_highscore,
                                  borderwidth=0,
                                  activebackground='#C0C0FF')
        highscore_btn.grid(row=2, column=0)

        # setup button
        img = Image.open('../images/marble_yellow_setup.png').resize((70, 70), Image.ANTIALIAS)
        self.setup_btn_image = ImageTk.PhotoImage(img)

        setup_btn = tk.Button(frame, width=75,
                              image=self.setup_btn_image,
                              bg='#C0C0FF',
                              relief='flat',
                              command=self.click_setup,
                              borderwidth=0,
                              activebackground='#C0C0FF')
        setup_btn.grid(row=3, column=1)

    def click_restart(self):
        print("Restart Button was pressed")

    def click_help(self):
        print("Help Button was pressed")

    def click_highscore(self):
        print("Highscore Button was pressed")

    def click_setup(self):
        print("Setup Button was pressed")


class Score:
    def __init__(self, frame):
        pass


class ActMarble:
    def __init__(self, frame):
        pass


class MarbleCounter:
    def __init__(self, frame):
        pass


class NextMarble:
    def __init__(self, frame):
        pass


# run Porygon
game = Game()
