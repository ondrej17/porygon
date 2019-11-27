import tkinter as tk


class Game:
    # dimension of window
    width_of_left = 600
    width_of_right = 200
    height = 960

    def __init__(self):
        # at the initialization create root object and window
        self.root = tk.Tk()
        self.root.title("Porygon")
        self.root.geometry("{}x{}".format(Game.width_of_left + Game.width_of_right, Game.height))

        self.window = Window(self.root)

        self.root.mainloop()

    # TODO: other methods for Game object


class Window:

    def __init__(self, root):
        self.root = root
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # create right frame that contains buttons, high-score, etc.
        self.right_frame = tk.Frame(self.main_frame,
                                    bg='grey',
                                    width=Game.width_of_right,
                                    height=Game.height)

        # create canvas aka playground
        self.playground = tk.Canvas(self.main_frame,
                                    bg='pink',
                                    width=Game.width_of_left,
                                    height=Game.height)

        # pack playground and right frame to main_frame
        self.right_frame.pack(side='right')
        self.playground.pack(side='left')

        # add background to playground
        self.image = tk.PhotoImage(file='../images/background.png')
        self.background = self.playground.create_image(Game.width_of_left/2, Game.height/2, image=self.image)

        # TODO: add stuff to the right frame


# run Porygon
Game()
