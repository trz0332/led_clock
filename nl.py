import time
def nl(x):
    utime_m=time.mktime((x[0],x[1],x[2],0,0,0,0,0))
    with open('nl_db') as file :
        st_m=file.readline(15)
        utime_c=time.mktime((int("20"+st_m[:2]),int(st_m[2:4]),int(st_m[4:6]),0,0,0,0,0))
        if utime_m<utime_c:
            return 000000
        else:
            seek_f=((utime_m-utime_c)//86400)*15
            file.seek(seek_f)
            rd_line=file.readline(20)
            return int(rd_line[7:13])

