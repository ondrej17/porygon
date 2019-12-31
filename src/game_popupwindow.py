import tkinter as tk


class UsernamePopupWindow:

    def __init__(self, parent):
        self.toplevel = tk.Toplevel(parent, height=300, width=300)
        self.username = tk.StringVar()

        label = tk.Label(self.toplevel, text="Enter username:")
        entry_field = tk.Entry(self.toplevel, textvariable=self.username)
        button = tk.Button(self.toplevel, text="Submit", command=self.toplevel.destroy)

        label.pack(side="top", fill="x", padx=10, pady=10)
        entry_field.pack(side="top", fill="x", padx=10, pady=10)
        button.pack(padx=10, pady=10)

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        value = self.username.get()
        return value


class AboutPopupWindow:

    def __init__(self, parent):
        self.toplevel = tk.Toplevel(parent, height=300, width=300)
        self.username = tk.StringVar()

        label = tk.Label(self.toplevel, text="Porygon Game")
        # TODO: add text to about window

        label.pack(padx=10, pady=10)


