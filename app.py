import tkinter as tk
from tkinter import Text, WORD, Button
from tkinter import ttk, Label, Scrollbar

TIME = 5


class App(tk.Tk):

    def __init__(self, title, size):
        super().__init__()

        # main setup
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(False, False)
        self.option_add('*Label.Font', 'Helvetica 20')
        self.option_add('*Text.Font', 'Helvetica 24')

        # main
        WelcomeMessage(parent=self).welcome_message()

        # run
        self.mainloop()

    def start_writing(self):
        TextInput(parent=self)


class WelcomeMessage(ttk.Frame):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent = parent

    def welcome_message(self):
        message = Label(self.parent,
                        text='Welcome to non stop writing app. Don’t stop writing, or all progress will be lost.',
                        fg='black',
                        wraplength=1000,
                        font='helvetica, 30')
        message.place(rely=0.1, relx=0.5, anchor='center')
        start_button = Button(self.parent, text='Start Writing', font='helvetica 24', command=self.start)
        start_button.place(rely=0.25, relx=0.5, anchor='center')

    def start(self):
        # destroy welcome message and button
        self.parent.place_slaves()[0].destroy()
        self.parent.place_slaves()[0].destroy()
        # init writing
        self.parent.start_writing()


class TextInput(ttk.Frame):

    def __init__(self, parent: App):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.create_widget(parent=parent)
        self.timer = 'zero'
        self.valid_keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o',
                           'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        self.parent = parent

    def create_widget(self, parent: App):
        main_text_input = Text(self, padx=24, pady=24, wrap=WORD)
        scroll_bar = ttk.Scrollbar(parent,
                                   orient='vertical',
                                   command=main_text_input.yview)
        main_text_input.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side='right', fill='y')
        main_text_input.place(relx=0, rely=0, relwidth=1, relheight=1)
        # automatically focus cursor on the input text
        main_text_input.focus_set()
        # trigger time counter on press key
        main_text_input.bind('<Key>', self.timer_start)

    def timer_start(self, event):
        if self.timer == 'zero' and event.char.lower() in self.valid_keys:
            self.timer = 0
            self.start_writing()
        else:
            self.reset_timer(event)

    def start_writing(self):
        self.timer += 1
        if self.timer <= TIME:
            self.after(1000, self.start_writing)
        else:
            self.destroy_text()

    def reset_timer(self, event):
        if event.char.lower() in self.valid_keys:
            self.timer = 0

    def destroy_text(self):
        self.parent.place_slaves()[0].destroy()
        self.parent.pack_slaves()[0].destroy()
        WelcomeMessage(parent=self.parent).welcome_message()
