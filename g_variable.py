import time
ntp_flag=False  #ntp连接成功表hi
temp=0.0  #获取到的温度
hum=0.0  #获取到的湿度
temp_old=0.0  #获取到的温度
hum_old=0.0  #获取到的湿度
QOS=1   #mqtt  qos
td_status='ON'   #灯开关状态
tcl=[(204,0,255)]*6  #初始灯的颜色
wuyiyi=0  #灯初始数字

mune=0  #菜单按键状态
up=0   #上按键
down=0  #下按键
jl_time=time.time()