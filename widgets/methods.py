class Methods:
    @staticmethod
    def one(val, operator):
        if operator == '+':
            val += 1
        elif operator == '-':
            val -= 1
        return val

    @staticmethod
    def ten(val, operator):
        if operator == '+':
            val += 10
        elif operator == '-':
            val -= 10
        return val

    @staticmethod
    def check(val, mi, ma):
        if mi <= val <= ma:
            return val
        if mi == 0:
            if val < mi:
                return ma + val + 1
            elif val > ma:
                return val - ma - 1
        else:
            if val < mi:
                return ma + val
            elif val > ma:
                return val - ma

    def __init__(self, master):
        self.master = master

    def unv_one(self, operator):
        self.master.universe = self.check(self.one(self.master.universe, operator), 1, 512)
        pass

    def unv_ten(self, operator):
        self.master.universe = self.check(self.ten(self.master.universe, operator), 1, 512)
        pass

    def adr_one(self, operator):
        self.master.address = self.check(self.one(self.master.address, operator), 1, 512)
        pass

    def adr_ten(self, operator):
        self.master.address = self.check(self.ten(self.master.address, operator), 1, 512)
        pass

    def val_one(self, operator):
        self.master.value = self.check(self.one(self.master.value, operator), 0, 255)
        pass

    def val_ten(self, operator):
        self.master.value = self.check(self.ten(self.master.value, operator), 0, 255)
        pass

    def set_val(self):
        self.master.scale_value = self.master.value
        self.master.data.universe = self.master.universe - 1
        self.master.data.send({self.master.address: self.master.scale_value})
        if self.master.scale_value == 0:
            self.master.not_null_value_address.discard(self.master.address)
        else:
            self.master.not_null_value_address.add(self.master.address)
        pass

    def reset(self):
        self.master.universe = 1
        self.master.address = 1
        self.master.value = 0
        self.zero()
        self.master.data.universe = self.master.universe - 1
        for adr in self.master.not_null_value_address:
            self.master.data.send({adr: 0})
        self.master.not_null_value_address.clear()
        pass

    def zero(self):
        self.master.scale_value = 0
        # self.master.undr.set(0)
        self.master.data.universe = self.master.universe - 1
        self.master.data.send({self.master.address: self.master.scale_value})
        self.master.not_null_value_address.discard(self.master.address)
        pass

    def full(self):
        self.master.scale_value = 255
        self.master.undr.set(255)
        self.master.data.universe = self.master.universe - 1
        self.master.data.send({self.master.address: self.master.scale_value})
        self.master.not_null_value_address.add(self.master.address)
        pass

    def settings(self):
        self.master.after(200, self.master.create_set_win())
        pass

    def default(self):
        pass

    def apply(self):
        self.close()
        pass

    def close(self):
        if self.master.name == 'app':
            self.reset()
        self.master.after(200, self.master.destroy)

    def scl_val(self):
        self.master.data.universe = self.master.universe - 1
        self.master.data.send({self.master.address: self.master.scale_value})
        if self.master.scale_value == 0:
            self.master.not_null_value_address.discard(self.master.address)
        else:
            self.master.not_null_value_address.add(self.master.address)
