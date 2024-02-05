import tkinter
from tkinter import *
from methods import Methods


class CustomFader(Label, Methods):
    def __init__(self, master, picture: str, atr=None, x=None, y=None, lnght=None, *args,**kward):
        super().__init__(master, *args, **kward)
        self.atr = atr
        self.x = x
        self.y = y
        self.lnght = lnght
        self.img1 = PhotoImage(file=f'pic//{picture}.png')
        self.img2 = PhotoImage(file=f'pic//{picture}2.png')
        self.create()

    def create(self):
        self.master.undr = Scale(self.master, foreground='#4D4C4C', bg='#4D4C4C', from_=255, to=0, length=self.lnght+30, command=self.scl_val, showvalue='0', border=1)
        self.master.undr.place(x=self.x+10, y=self.y-self.lnght+10)
    #     self.master.cvr = Label(self.master, image=self.img1, border=0, highlightthickness=0)
    #     self.master.cvr.place(x=self.x, y=self.y - self.master.scale_value)
    #     self.master.cvr.bind('<B1-Motion>', self.drag)
    #
        pass
    #
    # def drag(self, event):
    #     # print(15-event.y)
    #     self.master.scale_value = max(0, min(-(self.master.cvr.winfo_pointery() - self.master.cvr.winfo_rooty()), 255))
    #     self.master.after(100, self.master.cvr.place(y=self.y - self.master.scale_value))
    #     # self.master.undr.set(self.master.scale_value)
    #
    #     print(self.master.cvr.winfo_pointery() - self.master.cvr.winfo_rooty())



class CustomButton(CustomFader):
    def __init__(self, master, function=None, function_2=None, operator: str = None, *args, **kward):
        super().__init__(master, *args, **kward)
        self.function = function
        self.function_2 = function_2
        self.operator = operator
        self.configure(image=self.img1, border=0)
        self.create()
        self.binding()

    def create(self):
        self.place(x=self.x, y=self.y)

    def binding(self):
        self.bind('<Button-1>', self.button1_func)
        self.bind('<ButtonRelease-1>', lambda event: self.configure(image=self.img1))
        if self.function_2 is not None:
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

