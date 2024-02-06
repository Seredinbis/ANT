from tkinter import *
from methods import Methods


class CustomFader(Label, Methods):

    def __init__(self, master, picture: str, function=None, x=None, y=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.function = function
        self.x = x
        self.y = y
        self.start = self.y + 55
        self.img1 = PhotoImage(file=f'pic//{picture}.png')
        self.img2 = PhotoImage(file=f'pic//{picture}2.png')
        self.configure(image=self.img1, border=0)
        self.create()
        self.binding()

    def create(self):
        self.place(x=self.x, y=self.y)

    def binding(self):
        self.bind('<Button-1>', self.coord)
        self.bind('<B1-Motion>', self.button1_func)

    def button1_func(self, event):
        self.master.scale_value = max(0, min(-(event.y - self.start), 255))
        if self.master.scale_value % 2 == 0:
            self.configure(image=self.img1)
        else:
            self.configure(image=self.img2)
        getattr(self, self.function)()

    def coord(self, event):
        self.start = event.y + self.master.scale_value


class CustomButton(CustomFader):
    def __init__(self, master, function_2=None, operator: str = None, **kwargs):
        super().__init__(master, **kwargs)
        self.function_2 = function_2
        self.operator = operator
        if self.function_2 is not None:
            self.bind_2()

    def create(self):
        self.place(x=self.x, y=self.y)

    def binding(self):
        self.bind('<Button-1>', self.button1_func)
        self.bind('<ButtonRelease-1>', lambda event: self.configure(image=self.img1))

    def bind_2(self):
        self.bind('<Button-3>', self.button2_func)
        self.bind('<ButtonRelease-3>', lambda event: self.configure(image=self.img1))

    def button1_func(self, event):
        self.configure(image=self.img2)
        if self.operator is not None:
            getattr(self, self.function)(self.operator)
        else:
            getattr(self, self.function)()

    def button2_func(self, event):
        self.configure(image=self.img2)
        getattr(self, self.function_2)(self.operator)

