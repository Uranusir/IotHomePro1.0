#coding:utf-8

import serial
import time
import binascii


ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.5)    #串口初始化
print(ser.isOpen)
ADDR = [0x39,0x38]      #模块地址为全局变量


#########################################################################
# 功能：用于添加校验位
# 输入：除了校验位的整个数列
# 说明：校验位由包括包头在内的所有16进制数的和；
#       校验位是一位，所以每超过255减去256。
#########################################################################
def withParity(CMD):
    Parity = 0
    for bit in CMD:
        Parity = Parity + bit
        if Parity > 255:
            Parity = Parity - 256
    result = CMD + [Parity]
    print('校验后为：',result)
    return result



#########################################################################
# 功能：    向下位机发送指令
# 输入1：   CMDbit——命令编号
#           0x01——获取模块地址信息
#           0x12——红外线学习指令
#           0x14——红外线发射指令
# 输入2:    数据位——类型为队列；
#           无数据时输入空队列'''[]'''
# 说明：    五秒内接收不到数据就重发一次，再不行就标记失败
#########################################################################
def DataSend(CMDbit,DATA):          #DATA为列表
    CMDLong = len(DATA) + 5
    print('命令列表长为：',CMDLong)
    CMD = [0x7E]+[CMDLong]+[0x00]+ADDR+ADDR+[CMDbit]+DATA
    print('校验前为：',CMD)
    CMD = withParity(CMD)
    print('校验后为：',CMD)
    ser.write(CMD)

    counter=50
    while counter>-1:
        count = ser.inWaiting()
        if count != 0:
            time.sleep(0.5)
            Recv = ser.readline()
            print('接收数据为:',Recv)

            ser.flushInput()    #清理输入输出的缓存
            time.sleep(0.5)
            ser.flushOutput()
            time.sleep(0.5)

            return [hex(x) for x in bytes(Recv)]
        else:
            if counter<1:
                ser.write(CMD)
                print('超时重新发送：',CMD)
                counter = counter -1
            else:
                counter=counter-1
                if counter == 49:
                    print('等待数据：在5秒内重发')
        time.sleep(0.1)
    return 0

def serInit():
    print(ser.isOpen())
    if ser.isOpen() == False:
        print('串口未打开')
        ser.open()
        print('串口重新打开')
    else:
        print('串口准备就绪')
    time.sleep(0.5)
    ADDR = [0xFF,0xFF]
    ser.flushInput()
    time.sleep(0.5)
    ser.flushOutput()
    time.sleep(0.5)
    print('发送命令获取模块地址')
    result = DataSend(0x01,[])
    print(result)
    if result != 0:
        ADDR[0] = int(result[5],16)
        ADDR[1] = int(result[6],16)
        print('获取模块地址：',ADDR)
        return 1
    else:
        print('初始化失败')
        ser.close()
        print(ser.isOpen())
        return 0

if serInit()==0:
    print('程序错误')
else:
    CMD = input("输入动作")
    if CMD =='学习关灯':
        print(DataSend(0x12,[0x01,0x00]))   #学习1
    elif CMD == '关灯':
        print(DataSend(0x14,[0x01,0x00]))   #发射1
    elif CMD == '学习开灯':
        print(DataSend(0x12,[0x02,0x00]))   #学习2
    elif CMD == '开灯':
        print(DataSend(0x14,[0x02,0x00]))   #学习1
    elif CMD == '00':
        ser.close()
        serInit()
    elif CMD == '0':
        break
    else:
        continue
ser.close()