import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

import time

#定义通讯协议中的参数项
class SpnData:
    #data = 0
    #value = 0
    def __init__(self, name, addr,length,rate,offset,value=0):
        self.name = name
        self.addr = addr
        self.length = length
        self.rate = rate
        self.offset = offset
        self.value = value
        #print("name="+self.name)
        return

    def send(self):
        data_send = (self.value - self.offset) / self.rate
        return data_send
    def recv(self,data_recv):
        self.value = data_recv * self.rate + self.offset

#定义SpnTcpMaster类，TcpMaster增加方法
class SpnTcpMaster(modbus_tk.modbus_tcp.TcpMaster):
    _is_reconnect=False

    #def open(self):
    #    try:
    #        """open the communication with the slave"""
    #        if not self._is_opened:
    #            self._do_open()
    #            self._is_opened = True
    #            self._is_reconnect=False
    #    except modbus_tk.modbus_tcp.socket.error as e:
    #        self._is_opened=False
    #        self._is_reconnect=True
    #        print("连接网络: ",self._host," 失败，错误：",str(e))
    #    else:
    #        pass
    #    finally:
    #        pass

    def is_opened(self):
        return self._is_opened
    def is_reconnect(self):
        return self._is_reconnect
    def no_reconnect(self):
        self._is_reconnect=False
    def get_host(self):
        return self._host
    def set_host(self,host):
        self._host=host
    def read(self,spn_data,slave_id=1):
        try:
            if spn_data.length == 1:
                _data_format = ">h"            
            elif spn_data.length == 2:
                _data_format = ">i"
            else:
                pass
            spn_data.recv(self.execute(slave_id, cst.READ_HOLDING_REGISTERS, spn_data.addr, spn_data.length,data_format=_data_format)[0])
            #print("读取",spn_data.name,"值：",spn_data.value)
            return spn_data.value
        except modbus_tk.modbus.ModbusError as exc:
            self._is_opened=False
            self._is_reconnect=True
            print("%s- Code=%d", exc, exc.get_exception_code())
        except modbus_tk.modbus_tcp.socket.error as e:
            self._is_opened=False
            self._is_reconnect=True
            print("连接网络: ",self._host," 失败，错误：",str(e))
        else:
            pass
        finally:
            pass


    def write(self,spn_data,value,slave_id=1):
        try:
            spn_data.value=value
            self.execute(slave_id, cst.WRITE_MULTIPLE_REGISTERS, spn_data.addr,output_value=[int(spn_data.send())])
            print("写入",spn_data.name,"值：",spn_data.value)
        except modbus_tk.modbus.ModbusError as exc:
            self._is_opened=False
            self.is_reconnect=True
            print("%s- Code=%d", exc, exc.get_exception_code())
        except modbus_tk.modbus_tcp.socket.error as e:
            self._is_opened=False
            self.is_reconnect=True
            print("连接网络: ",self._host," 失败，错误：",str(e))
        else:
            pass
        finally:
            pass

'''待清理代码
#读数据
def modbus_read(master,spn_data,slave_id=1):
    
    spn_data.recv(master.execute(slave_id, cst.READ_HOLDING_REGISTERS, spn_data.addr, spn_data.length,data_format=">h")[0])
    #print("读取",spn_data.name,"值：",spn_data.value)


#写数据
def modbus_write(master,spn_data,slave_id=1):
    master.execute(slave_id, cst.WRITE_MULTIPLE_REGISTERS, spn_data.addr,output_value=[int(spn_data.send())])
    print("写入",spn_data.name,"值：",spn_data.value)
'''

#常量定义
MODBUS_TIMEOUT=5
steer_angle_set_manual = 10
robo_speed_set_manual_forward = 50
robo_speed_set_manual_backward = -50
robo_steer_angle_set_manual_left = 15
robo_steer_angle_set_manual_right = -15

#变量定义
master_robo = SpnTcpMaster()

#机器人参数定义
heartbeat = SpnData(name = "heartbeat",addr = 1000,length = 1,rate = 1,offset = 0)
robo_state = SpnData(name = "robo_state",addr = 1001,length = 1,rate = 1,offset = 0)
robo_id = SpnData(name = "robo_id",addr = 1002,length = 1,rate = 1,offset = 0)
soft_version = SpnData(name = "soft_version",addr = 1003,length = 1,rate = 1,offset = 0)
robo_speed = SpnData(name = "robo_speed",addr = 1004,length = 1,rate = 1,offset = 0)
steer_angle = SpnData(name = "steer_angle",addr = 1005,length = 1,rate = 0.0573,offset = 0)
bat_voltage = SpnData(name = "bat_voltage",addr = 1006,length = 1,rate = 0.1,offset = 0)
bat_soc = SpnData(name = "bat_soc",addr = 1007,length = 1,rate = 1,offset = 0)
bat_soh = SpnData(name = "bat_soh",addr = 1008,length = 1,rate = 1,offset = 0)
water_level = SpnData(name = "water_level",addr = 1009,length = 1,rate = 1,offset = 0)
distance_mark = SpnData(name = "distance_mark",addr = 1010,length = 1,rate = 1,offset = 0)
distance_last = SpnData(name = "distance_last",addr = 1011,length = 1,rate = 1,offset = 0)
mileage_hi = SpnData(name = "mileage_hi",addr = 1012,length = 1,rate = 1,offset = 0)
mileage_lo = SpnData(name = "mileage_lo",addr = 1013,length = 1,rate = 1,offset = 0)
chassis_state = SpnData(name = "chassis_state",addr = 1014,length = 1,rate = 1,offset = 0)
arm_state = SpnData(name = "arm_state",addr = 1015,length = 1,rate = 1,offset = 0)

#robo_speed   = SpnData(name = "robo_speed",addr = 1016,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 1017,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 1018,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 1019,length = 1,rate = 1,offset = 0)

ctrl_mode = SpnData(name = "ctrl_mode",addr = 2000,length = 1,rate = 1,offset = 0)
start_clean = SpnData(name = "start_clean",addr = 2001,length = 1,rate = 1,offset = 0)
drive_ctrl = SpnData(name = "drive_ctrl",addr = 2002,length = 1,rate = 1,offset = 0)
work_ctrl = SpnData(name = "work_ctrl",addr = 2003,length = 1,rate = 1,offset = 0)
arm_ctrl = SpnData(name = "arm_ctrl",addr = 2004,length = 1,rate = 1,offset = 0)
chassis_set = SpnData(name = "chassis_set",addr = 2005,length = 1,rate = 1,offset = 0)
time_plan = SpnData(name = "time_plan",addr = 2006,length = 1,rate = 1,offset = 0)

#robo_speed   = SpnData(name = "robo_speed",addr = 2007,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 2008,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 2009,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 2010,length = 1,rate = 1,offset = 0)
#heartbeat    = SpnData(name = "robo_speed",addr = 2011,length = 1,rate = 1,offset = 0)
#heartbeat    = SpnData(name = "robo_speed",addr = 2012,length = 1,rate = 1,offset = 0)
#heartbeat    = SpnData(name = "robo_speed",addr = 2013,length = 1,rate = 1,offset = 0)
#heartbeat    = SpnData(name = "robo_speed",addr = 2014,length = 1,rate = 1,offset = 0)

steer_angle_set = SpnData(name = "steer_angle_set",addr = 2015,length = 1,rate = 0.0573,offset = 0)
robo_speed_set = SpnData(name = "robo_speed_set",addr = 2016,length = 1,rate = 1,offset = 0)

#robo_speed   = SpnData(name = "robo_speed",addr = 2017,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 2018,length = 1,rate = 1,offset = 0)
#robo_speed   = SpnData(name = "robo_speed",addr = 2019,length = 1,rate = 1,offset = 0)








