import ntptime  #导入时间同步模块
from machine import RTC,Timer,Pin,I2C,freq
import time,network,json
from work import led_C  #导入6位LED灯模块
from sht20 import SHT20  #导入sht20模块
import utime  ,gc
import _thread  #导入多线程模块
from mqtt_as import MQTTClient  #导入mqtt模块
from mqtt_as import config
import uasyncio as asyncio  #导入异步模块
import g_variable    #导入一些自定义变量，用于全局变量
import cfg  #导入配置
import machine    
from ds3231 import DS3231    
freq(240000000) # set the CPU frequency to 240 MHz
rtc=RTC()
sta_if = network.WLAN(network.STA_IF)
ntptime.host=cfg.ntp_server


tc=led_C(cfg.led_pin)  #初始化LED灯模块
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
            tc.color_list=g_variable.tcl
            tc.show_num(tt)
        elif g_variable.mune==1:   #从111111到999999循环显示
            if g_variable.wuyiyi<999999:
                g_variable.wuyiyi+=111111
            else:g_variable.wuyiyi=0
            tc.show_num(g_variable.wuyiyi)
        elif g_variable.mune==2:   #显示日期
            localtime = time.localtime(time.time()+28800)
            localtime=localtime[0:3]
            azf=tc.fjie_num(localtime[0])
            tt=azf[-2]*100000+azf[-1]*10000+localtime[1]*100+localtime[2]
            tc.show_num(tt)
        elif g_variable.mune==3:   #全部点亮，由于60个灯全部点亮会造成电流过大实际，所以控制亮度位10
            for i in range(60):
                tc.np[i]=(10,10,10)
            tc.np.write()
        elif g_variable.mune==4:  #显示温度
            tt=tc.fjie_num(g_variable.temp*10)
            #print(tt)
            tc.show_list(tt)
        elif g_variable.mune==5:  #显示湿度
            tt=tc.fjie_num(g_variable.hum*10)
            tc.show_list(tt)
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
b3=Pin(cfg.b3_pin, Pin.IN, Pin.PULL_DOWN)
def tuch_mune():  #按钮1触发的时候
    g_variable.jl_time=time.time()
    if g_variable.td_status=='OFF':
        g_variable.td_status='ON'
        g_variable.tcl=[(204,0,255)]*6


    if  g_variable.mune<5:
        g_variable.mune+=1
    else :
        g_variable.mune=0
    #print(mune)
def pub_msg(topic, msg):  #推送mqtt消息
    if  client._has_connected:
        loop.create_task(client.publish(topic, msg, qos = g_variable.QOS))

def sub_cb(topic, msg, retained):  #订阅消息关联的函数
    try:
        ledmsg=json.loads(msg)
    except:
        print('json load err')
        pass
    else:
        if ('color' in ledmsg.keys()) and ('state' in ledmsg.keys()) :
            if ledmsg['state']=='ON':
                for i in range(6):
                    g_variable.tcl[i]=(ledmsg['color']['r'],ledmsg['color']['g'],ledmsg['color']['b'])
                g_variable.td_status='ON'
            else:
                g_variable.td_status='OFF'
                tc.np.fill((0,0,0))
                tc.np.write()
        elif ('list' in ledmsg.keys()) and ('state' in ledmsg.keys()) :
            if ledmsg['state']=='ON':
                for i in range(6):
                    g_variable.tcl[i]=(ledmsg['color']['r'],ledmsg['color']['g'],ledmsg['color']['b'])
                g_variable.td_status='ON'
            else:
                g_variable.td_status='OFF'
                tc.np.fill((0,0,0))
                tc.np.write()
        elif ('state' in ledmsg.keys()) :
            if ledmsg['state']=='ON':
                g_variable.tcl=g_variable.tcl
            elif ledmsg['state']=='OFF':
                tc.np.fill((0,0,0))
                tc.np.write()
            g_variable.td_status=ledmsg['state']
        tc.color_list=g_variable.tcl
        update()

def updatehj():  #推送温湿度数据
    pub_msg(cfg.topic_hjdata,json.dumps({'temp':str(g_variable.temp),'hum':str(g_variable.hum)})  )
    
def update():   #推送led灯状态数据
    msg = json.dumps({'state':g_variable.td_status,'color':{'r':tc.np[0][0],'g':tc.np[0][1],'b':tc.np[0][2]}})
    pub_msg(topic_rbg_stat,msg)


time_show_lcd=Timer(0)   #定时器刷新led灯  不要设置的太快了，micropython的运算速度太慢，
time_show_lcd.init(period=100, mode=Timer.PERIODIC, callback=lambda t:show_l_t())
time_init_datetime=Timer(1)   #定时器同步时间
time_init_datetime.init(period=3600000, mode=Timer.PERIODIC, callback=lambda t:init_upttime())
time_get_sht20=Timer(2)  #定时器获取温度
time_get_sht20.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:get_sht20())
time_updathj=Timer(3)   #定时器推送温湿度数据
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
