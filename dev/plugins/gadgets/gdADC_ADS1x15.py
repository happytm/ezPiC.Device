"""
Gadget Plugin for ADC ADS1x15
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdADS1x15'
PTYPE = PT_SENSOR
PNAME = '@PLAN ADC - ADS1015, ADS1115 - 4-Ch 12/16-Bit ADC (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'ADS1x15',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'48',
            # instance specific params
            'RespVar0':'Channel0',
            'RespVar1':'Channel1',
            'RespVar2':'Channel2',
            'RespVar3':'Channel3',
            'FSR':'0',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        if self._i2c and self.param['InitVal']:
            self._i2c.write_byte(int(self.param['InitVal'], 0))

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('48 (ADDR-GND)', '49 (ADDR-VDD)', '4A (ADDR-SDA)', '4B (ADDR-SCL)')

# -----

    def variables(self, news:dict):
        if not self._i2c:
            return

        try:
            name = self.param['TrigVar']
            if name and name in news:
                val = Variable.get(name)
                if type(val) == str:
                    val = int(val, 0)
                if 0 <= val <= 255:
                    self._i2c.write_byte(val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

# -----

    def timer(self, prepare:bool):
        if not self._i2c:
            return

        try:
            name = self.param['RespVar']
            if name:
                val = self._i2c.read_byte()
                print(val)
                if val != self._last_val:
                    self._last_val = val
                    Variable.set(name, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######