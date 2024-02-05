from tkinter import *
from tkinter import ttk
from custom_widgets import CustomButton, CustomFader
from artnet.widget_enter import CheckData


class Window(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Ethernet settings')
        self.geometry('403x251+400+380')
        self.resizable(False, False)
        self.bg_img = PhotoImage(file='pic//bg_set.png')
        Label(self, image=self.bg_img).pack()
        self.dif_x = 0
        self.dif_y = 0
        self.overrideredirect(True)
        self.create_widgets()

    def create_widgets(self):
        CustomButton(self, picture='def', function='default', x=41, y=190)
        CustomButton(self, picture='apl', function='apply', x=213, y=190)
        pass


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('ANT v 1.0')
        self.geometry('575x355+300+300')
        self.resizable(False, False)
        self.overrideredirect(True)
        self.wm_attributes('-topmost', True)
        self.bg_im = PhotoImage(file='pic//win.png')
        Label(self, image=self.bg_im).pack()
        self.set_win = None
        self._universe = 1
        self._address = 1
        self._value = 0
        self._scale_value = 0
        self.style = ttk.Style()
        self.style.configure('TLabel', bg='#A2A7A1', font='Tahoma 20', fg='#4D4C4C')
        self.universe_label = ttk.Label()
        self.address_label = ttk.Label()
        self.value_label = ttk.Label()
        self.scale_value_label = ttk.Label()
        self.percent_label = ttk.Label()
        self.create_widgets()
        self.data = CheckData()

    def create_widgets(self):
        self.universe_label.config(text='{:03d}'.format(self._universe))
        self.universe_label.place(x=74, y=52)
        self.address_label.config(text='{:03d}'.format(self._address))
        self.address_label.place(x=74, y=137)
        self.value_label.config(text='{:03d}'.format(self._value))
        self.value_label.place(x=74, y=222)
        self.scale_value_label.config(text='{:03d}'.format(int(self._scale_value)))
        self.scale_value_label.place(x=480, y=52)
        self.percent_label.config(text='{:03d}'.format(int(self._scale_value // 2.55)))
        self.percent_label.place(x=480, y=137)
        CustomButton(self, picture='unv_up', function='unv_one', function_2='unv_ten', operator='+', x=132, y=50)
        CustomButton(self, picture='unv_dwn', function='unv_one', function_2='unv_ten', operator='-', x=25, y=50)
        CustomButton(self, picture='adr_up', function='adr_one', function_2='adr_ten', operator='+', x=132, y=135)
        CustomButton(self, picture='adr_dwn', function='adr_one', function_2='adr_ten', operator='-', x=25, y=135)
        CustomButton(self, picture='val_up', function='val_one', function_2='val_ten', operator='+', x=132, y=220)
        CustomButton(self, picture='val_dwn', function='val_one', function_2='val_ten', operator='-', x=25, y=220)
        CustomButton(self, picture='set', function='set_val', x=200, y=220)
        CustomButton(self, picture='res', function='reset', x=25, y=290)
        CustomButton(self, picture='zer', function='zero', x=200, y=290)
        CustomButton(self, picture='ful', function='full', x=273, y=290)
        CustomButton(self, picture='sets', function='settings', x=461, y=290)
        CustomButton(self, picture='pow', function='close', x=511, y=290)
        CustomFader(self, picture='fdr', atr='scale_value', x=391, y=280, lnght=255)
        pass

    def create_set_win(self):
        self.set_win = Window(self)

    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, val):
        self._universe = val
        self.universe_label.configure(text='{:03d}'.format(self._universe))

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, val):
        self._address = val
        self.address_label.configure(text='{:03d}'.format(self._address))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.value_label.configure(text='{:03d}'.format(self._value))

    @property
    def scale_value(self):
        return self._scale_value

    @scale_value.setter
    def scale_value(self, val):
        self._scale_value = val
        self.scale_value_label.configure(text='{:03d}'.format(int(self._scale_value)))
        self.percent_label.config(text='{:03d}'.format(int(self._scale_value // 2.55)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
