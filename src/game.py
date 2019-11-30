import random
import tkinter as tk


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
        self.score = Score(self.main_frame)
        self.control_buttons = ControlButtons(self.main_frame)

        # TODO: add canon, next marbles to the playground
        self.act_marble = ActMarble(self.main_frame)
        self.next_marble_counter = MarbleCounter(self.main_frame)
        self.next_marble_color = NextMarble(self.main_frame)

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
            self.pictures[color] = tk.PhotoImage(file=name_of_picture)


class Score:
    def __init__(self, frame):
        pass


class ControlButtons:
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
