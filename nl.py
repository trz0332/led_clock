import time

def nl(x):
    utime_m=time.mktime((x[0],x[1],x[2],0,0,0,0,0))
    if utime_m<649468800:
        return 000000
    else:
        seek_f=((utime_m-649468800)//86400)*15
        with open('nl_db') as file :
            sa=file.seek(seek_f)
            rd_line=file.readline(20)
    return rd_line[7:13]

