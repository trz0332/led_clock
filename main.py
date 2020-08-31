import ntptime  #导入时间同步模块
from machine import RTC,Timer,Pin,I2C,freq
import time,network,json
from work_spi import led_C  #导入6位LED灯模块
from sht20 import SHT20  #导入sht20模块
import utime  ,gc
from random import randrange,choice
import _thread  #导入多线程模块
from mqtt_as import MQTTClient  #导入mqtt模块
from mqtt_as import config
import uasyncio as asyncio  #导入异步模块
import g_variable    #导入一些自定义变量，用于全局变量
import cfg  #导入配置
import machine    
from ds3231 import DS3231   
from nl import nl 
freq(160000000) # set the CPU frequency to 240 MHz
rtc=RTC()
sta_if = network.WLAN(network.STA_IF)
ntptime.host=cfg.ntp_server


tc=led_C(cfg.led_pin)  #初始化LED灯模块
tc.color_list=g_variable.tcl #初始化LED灯颜色
i2_bus=I2C(1,scl=Pin(cfg.i2c_scl_pin), sda=Pin(cfg.i2c_sda_pin), freq=100000)  #初始化I2C总线
sht=SHT20(i2_bus)  #
ds32=DS3231(i2_bus)
def get_sht20():  #获取温湿度
    if 64 in i2_bus.scan():
        g_variable.temp=round(sht.get_temperature(),1)
        g_variable.hum=round(sht.get_relative_humidity(),1)
        if  abs(g_variable.temp-g_variable.temp_old)>0.5 or abs(g_variable.hum-g_variable.old_hum)>10:
            updatehj()
            g_variable.old_temp=g_variable.temp
            g_variable.old_hum=g_variable.hum


    



def init_upttime():  #时间同步
    try:
        ntptime.settime()
    except:
        g_variable.ntp_flag=False
        rtc.datetime(tuple(ds32.datetime()+[0]))
    else:   #如果
        g_variable.ntp_flag= True
        ds32.datetime(list(rtc.datetime())[-1])

    #print(time.localtime(time.time()+28800))



def show_l_t():  #led显示函数
    if  g_variable.td_status == 'ON':
        if g_variable.mune==0:   #显示时间
            localtime = time.localtime(time.time()+28800)
            localtime=localtime[3:6]
            tt=localtime[0]*10000+localtime[1]*100+localtime[2]
            #tc.color_list=g_variable.tcl
            tc.show_num(tt)
        elif g_variable.mune==1:  #显示随机数
            if g_variable.up==0:
                tc.show_num(randrange(0,999999))


        elif g_variable.mune==2:   #显示日期
            localtime = time.localtime(time.time()+28800)
            localtime=localtime[0:3]
            azf=tc.fjie_num(localtime[0])
            tt=azf[-2]*100000+azf[-1]*10000+localtime[1]*100+localtime[2]
            tc.show_num(tt)
        elif g_variable.mune==3:   #显示日期
            tt=nl(time.localtime(time.time()+28800))
            tc.show_num(int(tt))

        elif g_variable.mune==4:   #全部点亮，由于60个灯全部点亮会造成电流过大实际，所以控制亮度位10
            tc.np.show([(10,10,10)]*60)
        elif g_variable.mune==5:  #显示温度
            tt=tc.fjie_num(g_variable.temp*10)
            #print(tt)
            tc.show_list(tt)
        elif g_variable.mune==6:  #显示湿度
            tt=tc.fjie_num(g_variable.hum*10)
            tc.show_list(tt)
        elif g_variable.mune==7:   #从111111到999999循环显示
            if g_variable.wuyiyi<999999:
                g_variable.wuyiyi+=111111
            else:g_variable.wuyiyi=0
            if g_variable._index !=0:
                g_variable.wuyiyi=zh(g_variable.wuyiyi,g_variable._index-1)
            """
            ##想设置颜色渐变，还没有办法实现
            if g_variable.r>255:
                g_variable.r=0
                g_variable.b=
            """
            tc.show_num(g_variable.wuyiyi)
        elif g_variable.mune==9999:  #显示mqtt传来的60位led颜色数据
            tc.np.write()
        elif g_variable.mune==8888:  #显示mqtt传来的6位整型数据
            tc.show_num(g_variable.show_num)
    if g_variable.mune !=0 and (time.time()-g_variable.jl_time)>60  :g_variable.mune=0
    #update()  #mqtt更新灯状态
    

def connect_wifi():  #连接wifi
    sta_if.active(True)
    sta_if.scan()                             # Scan for available access points
    try:
        sta_if.connect(cfg.ssid,cfg.wifi_pw) # Connect to an AP
    except:pass
    else:sta_if.config(dhcp_hostname=cfg.sysname)
    return sta_if.isconnected() 
connect_wifi()  #第一次连接wifi
init_upttime()
b1=Pin(cfg.b1_pin, Pin.IN, Pin.PULL_DOWN)
b1.irq(lambda p:tuch_mune(), trigger=(Pin.IRQ_RISING))  #按钮1上升沿中断
b2=Pin(cfg.b2_pin, Pin.IN, Pin.PULL_DOWN)
b2.irq(lambda p:tuch_up(), trigger=(Pin.IRQ_RISING))  #按钮1上升沿中断
b3=Pin(cfg.b3_pin, Pin.IN, Pin.PULL_DOWN)
b3.irq(lambda p:tuch_down(), trigger=(Pin.IRQ_RISING))  #按钮1上升沿中断

def ffdd_up(m_list):
    if len(m_list)-1>g_variable._index>=0:g_variable._index+=1
    else:g_variable._index=0
    #print(m_list[g_variable._index])
    return m_list[g_variable._index]

def ffdd_down(m_list):

    if len(m_list)-1>=g_variable._index>0:g_variable._index-=1
    else:g_variable._index=len(m_list)-1
    return m_list[g_variable._index]

def zh(a,b):  #这个函数主要是用于10进制的与0
    c=tc.fjie_num(a)
    c[b]=0
    d=0
    for index,item in enumerate(c):
        d+=item*(pow(10,5-index))
    return d

def tuch_mune():  #按钮1触发的时候
    g_variable.jl_time=time.time()
    g_variable._index=0
    g_variable.up=0
    if g_variable.td_status=='OFF':
        g_variable.td_status='ON'
        g_variable.tcl=[(204,0,255)]*6

    if  g_variable.mune<7:
        g_variable.mune+=1
    else :
        g_variable.mune=0
def tuch_up():
    g_variable.jl_time=time.time()
    if g_variable.mune==1   :
        g_variable.up=ffdd_up(g_variable.time_line_mune)
        if g_variable.up ==1:
            tc.show_num(choice(g_variable.time_line))
    elif g_variable.mune==0   :
        if g_variable.td_status=='ON':
            g_variable.td_status='OFF'
            tc.np.show([])
        update()
    elif g_variable.mune==7   :
        g_variable._index1=0
        if  g_variable._index<6:
            g_variable._index+=1
        else :
            g_variable._index=0
    


def tuch_down():
    g_variable.jl_time=time.time()
    if g_variable.mune==1   :
        g_variable.up=ffdd_down(g_variable.time_line_mune)
        if g_variable.up ==1:
            tc.show_num(choice(g_variable.time_line))
    elif g_variable.mune==0   :
        if g_variable.td_status=='OFF':
            g_variable.td_status='ON'
        update()

    elif g_variable.mune==7   :
        #max_len=len(g_variable.tcl_1)
        if g_variable._index1<g_variable.mune6_max_index1-1:
            g_variable._index1+=1
        else:g_variable._index1=0

        if g_variable._index==0:
            for index,item in enumerate(g_variable.tcl_1[g_variable._index1]):
                tc.color_list[index]= item
            #print(g_variable.tcl_2)
            g_variable.mune6_max_index1=len(g_variable.tcl_1)
        else:
            g_variable.mune6_max_index1=len(g_variable.tcl_2)
            tc.color_list[g_variable._index-1]=g_variable.tcl_2[g_variable._index1]
        #print(g_variable._index,g_variable._index1)



    #print(mune)
def pub_msg(topic, msg):  #推送mqtt消息
    if  client._has_connected:
        loop.create_task(client.publish(topic, msg, qos = g_variable.QOS))
def is_listcolor(list1):
    if type(list1)==list and len(list1)==6:
        for i in list1:
            for x in i :
                if x >255 or x <0 :
                    return False
        return True
    else :return False

def sub_cb(topic, msg, retained):  #订阅消息关联的函数
    try:
        ledmsg=json.loads(msg)
        #print(ledmsg)
    except:
        print('json load err')
        pass
    else:
        if ('color' in ledmsg.keys()) and ('state' in ledmsg.keys()) :   #传递单个颜色
            if ledmsg['state']=='ON':
                for i in range(6):
                    g_variable.tcl[i]=(ledmsg['color']['r'],ledmsg['color']['g'],ledmsg['color']['b'])
                g_variable.td_status='ON'
            else:
                g_variable.td_status='OFF'
                tc.np.show([])
            tc.color_list=g_variable.tcl
        elif ('list' in ledmsg.keys()) and ('state' in ledmsg.keys()) :  #传递6个颜色
            if ledmsg['state']=='ON' :
                if  is_listcolor(ledmsg['list']):
                    g_variable.tcl=ledmsg['list']
                    g_variable.td_status='ON'
            else:
                g_variable.td_status='OFF'
                tc.np.show([])
            tc.color_list=g_variable.tcl
        elif ('c_data' in ledmsg.keys()) and ('state' in ledmsg.keys()) :   #传递60位颜色
            if ledmsg['state']=='ON' :
                try:
                    g_variable.jl_time=time.time()
                    tc.np.data=ledmsg['data']
                except Exception as e:
                    print(e)
                else:
                    g_variable.mune=9999
            else:
                g_variable.td_status='OFF'
                tc.np.show([])

        elif ('d_data' in ledmsg.keys()) and ('state' in ledmsg.keys()) :  #传递6位数字
            if ledmsg['state']=='ON' :
                try:
                    g_variable.jl_time=time.time()
                    g_variable.show_num=int(ledmsg['d_data'])
                    #print(g_variable.show_num)
                except Exception as e:
                    print(e)
                else:
                    g_variable.mune=8888
            else:
                g_variable.td_status='OFF'
                tc.np.show([])



        elif ('state' in ledmsg.keys()) :
            if ledmsg['state']=='ON':
                g_variable.tcl=g_variable.tcl
            elif ledmsg['state']=='OFF':
                tc.np.show([])
            g_variable.td_status=ledmsg['state']
            tc.color_list=g_variable.tcl

        
        update()

def updatehj():  #推送温湿度数据
    pub_msg(cfg.topic_hjdata,json.dumps({'temp':str(g_variable.temp),'hum':str(g_variable.hum)})  )
    
def update():   #推送led灯状态数据
    if len(tc.np.data)==0:msg = json.dumps({'state':g_variable.td_status,'color':{'r':0,'g':0,'b':0}})
    else:
        msg = json.dumps({'state':g_variable.td_status,'color':{'r':tc.np.data[0][0],'g':tc.np.data[0][1],'b':tc.np.data[0][2]}})
    pub_msg(topic_rbg_stat,msg)


time_show_lcd=Timer(3)   #定时器刷新led灯  不要设置的太快了，micropython的运算速度太慢，
time_show_lcd.init(period=50, mode=Timer.PERIODIC, callback=lambda t:show_l_t())
time_init_datetime=Timer(1)   #定时器同步时间
time_init_datetime.init(period=3600000, mode=Timer.PERIODIC, callback=lambda t:init_upttime())
time_get_sht20=Timer(2)  #定时器获取温度
time_get_sht20.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:get_sht20())
time_updathj=Timer(0)   #定时器推送温湿度数据
time_updathj.init(period=180000, mode=Timer.PERIODIC, callback=lambda t:updatehj())
async def conn_han(client):
    await client.subscribe(topic_rbg_command, g_variable.QOS)
    pub_msg(cfg.topic_status,'Connected')

async def main(client):  #mqtt主循环
    await client.connect()
    while True:
        await asyncio.sleep(60)
        if not g_variable.ntp_flag:
            init_upttime()   #第一次同步时钟
            if g_variable.ntp_flag:ds32.datetime(list(rtc.datetime())[-1])

topic_rbg_stat=cfg.topic_rbg_stat
topic_rbg_command=cfg.topic_rbg_command
topic_hjdata=cfg.topic_hjdata
topic_status=cfg.topic_status
config['server'] = cfg.mqtt_server
config['ssid'] = cfg.ssid
config['wifi_pw'] = cfg.wifi_pw
config['user'] = cfg.user
config['password'] =  cfg.password

config['subs_cb'] = sub_cb
config['connect_coro'] = conn_han
client = MQTTClient(config)
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
loop = asyncio.get_event_loop()
update()
updatehj()
get_sht20()
gc.collect()
try:
    loop.run_until_complete(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
