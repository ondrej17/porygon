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

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Porygon")
        self.root.geometry("{}x{}".format(self.playground_width + self.right_toolbar_width,
                                          self.right_toolbar_height + self.bottom_toolbar_height))
        self.root.resizable(False, False)
        self.main_frame = tk.Frame(self.root, bg='SlateGray1')
        self.main_frame.pack(expand=True)

        # create playground, bottom and right toolbar
        self.playground = tk.Canvas(self.main_frame,
                                    bg='SlateGray1',
                                    width=self.playground_width-20,
                                    height=self.playground_height-20,
                                    relief='sunken',
                                    borderwidth=5)

        self.bottom_toolbar = tk.Frame(self.main_frame,
                                       bg='SlateGray1',
                                       width=self.bottom_toolbar_width,
                                       height=self.bottom_toolbar_height)

        self.right_toolbar = tk.Frame(self.main_frame,
                                      bg='SlateGray1',
                                      width=self.right_toolbar_width,
                                      height=self.right_toolbar_height)
        self.about_frame = tk.Frame(self.main_frame,
                                    bg='SlateGray1',
                                    width=self.right_toolbar_width,
                                    height=self.bottom_toolbar_height)

        # pack playground and right frame to main_frame
        self.playground.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        self.right_toolbar.grid(row=0, column=1, padx=0, pady=0, sticky='ne')
        self.bottom_toolbar.grid(row=1, column=0, padx=0, pady=0, sticky='sw')
        self.about_frame.grid(row=1, column=1, padx=0, pady=0, sticky='se')

        # add a marble to playground
        self.marble_blue = tk.PhotoImage(file="../images/marble_blue.png")
        self.playground.create_image(100, 100, image=self.marble_blue)

        # TODO: add stuff to the right frame
        self.score = Score(self.main_frame)
        self.control_buttons = ControlButtons(self.main_frame)

        # TODO: add canon, next marbles to the playground
        self.act_marble = ActMarble(self.main_frame)
        self.next_marble_counter = MarbleCounter(self.main_frame)
        self.next_marble_color = NextMarble(self.main_frame)

        # at the end of __init__
        self.root.mainloop()


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
Game()
