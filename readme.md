主控esp32  
用micropython实现  
用led模拟辉光时钟  
可以显示温度，湿度，时间，日期  
使用ntp自动对时  
![image](https://github.com/trz0332/led_clock/blob/master/led_.jpg?raw=true)
增加用mqtt设置灯的颜色
这个命令是直接设置60位LED灯的颜色的命令  
mosquitto_pub -u pi -P passwd -t ''home/rgb1/set'' -m '{"data": [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], "state": "ON"}'  
这个命令是设置6位数字灯的颜色的命令，所有数字颜色相同  
mosquitto_pub -u pi -P passwd -t ''home/rgb1/set'' -m '{"color": {"r": 255, "g": 255, "b": 255},"state":"ON"}'  
这个命令是设置显示6位数字的命令  
mosquitto_pub -u pi -P passwd -t ''home/rgb1/set'' -m '{"d_date": 123456,"state":"ON"}'  
这个是设置6位数字颜色的命令，数字颜色可以不同  
mosquitto_pub -u pi -P passwd -t ''home/rgb1/set'' -m '{"list": [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],],"state":"ON"}'    
增加农历显示，    
使用3个按键，可以用按键设置颜色。颜色配置列表在g_variable.py中设置tcl_1里面预填了几种颜色，这里面的颜色是设置所有灯的颜色  
tcl_2里面的颜色是单个灯的颜色的预约设置  
  
添加了时间线设置。进入时间线设置会随机显示数字，当按下up或者down键的时候，可以随机显示时间线，预约时间线设置是在g_variable.py里面的time_line  
