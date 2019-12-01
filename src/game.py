from game_window import Window
from game_popupwindow import PopupWindow


class Game:
    def __init__(self):

        # at the beginning show popup windows for entering username
        pop = PopupWindow()

        # load username from popup window (after 'Enter' key is pressed, it gets killed)
        self.username = pop.get_username()

        # create window object (actual game)
        self.window = Window(self.username)

    # TODO: other methods for Game object
    #  e.g. timer
