import tkinter

class Program:
    def __init__(self):
        # don't change canvas dimensions
        self.canvas = tkinter.Canvas(width=800, height=960, bg='black')
        self.canvas.pack()

        self.background = tkinter.PhotoImage(file='background.png')
        self.canvas.create_image(300, 480, image=self.background)
        tkinter.mainloop()


Program()

# creating different types of ball
# ball_blue = tkinter.PhotoImage(file='marble_blue.png')
# ball_yellow = tkinter.PhotoImage(file='marble_yellow.png')
# ball_red = tkinter.PhotoImage(file='marble_red.png')
