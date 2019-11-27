import tkinter as tk


class Window:
    width_of_left = 600
    width_of_right = 200
    height = 960

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Porygon")
        self.root.geometry("{}x{}".format(self.width_of_left + self.width_of_right, self.height))
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # create toolbar that contains buttons, high-score, etc.
        self.toolbar = tk.Canvas(self.main_frame,
                                 bg='cornflowerblue',
                                 width=self.width_of_right,
                                 height=self.height)

        # create canvas aka playground
        self.playground = tk.Canvas(self.main_frame,
                                    bg='pink',
                                    width=self.width_of_left,
                                    height=self.height)

        # pack playground and right frame to main_frame
        self.toolbar.pack(side='right')
        self.playground.pack(side='left')

        # add background to playground
        self.image = tk.PhotoImage(file='../images/background.png')
        self.background = self.playground.create_image(self.width_of_left / 2, self.height / 2, image=self.image)

        # TODO: add stuff to the right frame
        self.highscore = Highscore(self.toolbar)
        self.score = Score(self.toolbar)
        self.buttons = Buttons(self.toolbar)

        # TODO: add canon, next marbles to the playground
        self.canon = Canon(self.playground)
        self.cartridge = Cartridge(self.playground)

        # at the end of __init__
        self.root.mainloop()


class Canon:
    def __init__(self, playground):
        pass


class Cartridge:
    def __init__(self, playground):
        pass


class Highscore:
    def __init__(self, toolbar):
        pass


class Score:
    def __init__(self, toolbar):
        pass


class Buttons:
    def __init__(self, toolbar):
        pass


class Marble:
    def __init__(self):
        pass