import tkinter as tk
from PIL import Image, ImageTk


class ControlButtons:
    def __init__(self, frame):
        # width of buttons must be together equal to right_toolbar_width from Window

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
        self.score = 0

        self.score_label = tk.Label(frame, text='Score', font='Arial 15', bg='#C0C0FF')
        self.score_label.grid(row=5, column=0, columnspan=2)

        self.score_value = tk.Label(frame, text="{}".format(self.score), font='Arial 15', bg='#C0C0FF')
        self.score_value.grid(row=6, column=0, columnspan=2)

    def add_to_score(self, score):
        self.score += score
        self.score_value.update()

    def get_score(self):
        return self.score


class ActMarble:
    def __init__(self, frame):
        pass


class MarbleCounter:
    def __init__(self, frame):
        pass


class NextMarble:
    def __init__(self, frame):
        pass
