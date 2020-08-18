from time import sleep_ms
TRI_T_MEASURE_NO_HOLD = b'\xf3'
TRI_RH_MEASURE_NO_HOLD = b'\xf5'
from struct import unpack as unp
SHT20_I2CADDR = 64
class SHT20(object):
    def __init__(self, _bus):
        self._address = SHT20_I2CADDR
        self._bus = _bus
    def get_temperature(self):
        self._bus.writeto(self._address, TRI_T_MEASURE_NO_HOLD)
        sleep_ms(150)
        origin_data = self._bus.readfrom(self._address, 2)
        origin_value = unp('>h', origin_data)[0]
        value = -46.85 + 175.72 * (origin_value / 65536)
        return value
    def get_relative_humidity(self):
        self._bus.writeto(self._address, TRI_RH_MEASURE_NO_HOLD)
        sleep_ms(150)
        origin_data = self._bus.readfrom(self._address, 2)
        origin_value = unp('>H', origin_data)[0]
        value = -6 + 125 * (origin_value / 65536)
        return value  