from machine import Pin
from neopixel import NeoPixel
import time

class led_C:
    def __init__(self,pin):
        self.pin=Pin(pin, Pin.OUT)
        self.np=NeoPixel(self.pin, 60)
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
        self.np.fill((0,0,0))
        for index,item in enumerate(numlist):
            self.np[index*10+item]=self.color_list[index]
        self.np.write()
    def show_list(self,list1):
        self.np.fill((0,0,0))
        for index,item in enumerate(list1):
            self.np[index*10+item]=self.color_list[index]
        self.np.write()

if __name__=='__main__':
    ts=led_C()
    for i in range(100000):
        ts.show_num(i)
        #time.sleep(0.01)
