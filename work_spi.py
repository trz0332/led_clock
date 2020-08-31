from machine import Pin,SPI
from ws2812 import WS2812
import time

class led_C:
    def __init__(self,pin):
        #self.np=NeoPixel(self.pin, 60)
        self.np=WS2812(SPI(1, 3200000, sck=Pin(14), mosi=Pin(pin), miso=Pin(12)),60)
        self.color=(255, 255, 255)
        self.num=0
        self.color_list=[self.color,self.color,self.color,self.color,self.color,self.color]


    def fjie_num(self,value):
        result = []
        while value:
            value, r = divmod(value, 10)
            result.append(int(r))
        #result.reverse()
        if len(result)<6:
            result+=[0]*(6-len(result))
        elif len(result)>6:
            result=result[(len(result)-6):]
        result.reverse()
        return result
    def show_num(self,num):
        numlist=self.fjie_num(num)
        #self.np.show([])
        self.np.data=[(0,0,0)]*60
        for index,item in enumerate(numlist):
            self.np.data[index*10+item]=self.color_list[index]
        self.np.write()
    def show_list(self,list1):
        #self.np.show([])
        self.np.data=[(0,0,0)]*60
        for index,item in enumerate(list1):
            self.np.data[index*10+item]=self.color_list[index]
        self.np.write()

