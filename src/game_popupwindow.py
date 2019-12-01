import tkinter as tk


class PopupWindow(object):
    width = 300
    height = 200

    def __init__(self):
        # create root Tk object and set its properties
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.resizable(False, False)

        # create MAIN FRAME and set its properties
        self.main_frame = tk.Frame(self.root, bg='#C0C0FF')
        self.main_frame.pack(expand=True, fill='both')

        # bind <Return> key to method 'kill_myself'
        self.root.bind('<Return>', self.kill_myself)

        # layout components popup window
        # create label
        self.label = tk.Label(self.main_frame, text='Enter you username:', font='Arial 12', bg='#C0C0FF')
        self.label.pack(padx=3, pady=20)

        # create 'entry' object (username will be typed here)
        self.username = tk.StringVar()
        self.entry = tk.Entry(self.main_frame, textvariable=self.username)
        self.entry.pack(padx=3, pady=20)

        # set focus on entry widget (you can type immediately)
        self.entry.focus()

        # add 'Enter' button, so you can submit typed username
        # clicking on this button, popup windows kill itself
        self.button = tk.Button(self.main_frame, text='Enter', command=self.root.destroy)
        self.button.pack(padx=3, pady=20)

        # at the end of __init__
        self.root.mainloop()

    def get_username(self):
        """
        returns typed username that is later used in game
        """
        return self.username.get()

    def kill_myself(self, event):
        """
        closes popup window if only if there is username typed in entry object
        """
        if self.username.get() != "":  # .... .get() is here due to StringVar() object
            self.root.destroy()



