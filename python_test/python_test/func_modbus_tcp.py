import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

import time

#定义通讯协议中的参数项
class SpnData(object):
    def __init__(self, name, addr,length,rate,offset,rw="r",value=0):
        self.name = name
        self.addr = addr
        self.length = length
        self.rate = rate
        self.offset = offset
        self.value = value
        self.rw=rw
        return

    def send(self):
        data_send = (self.value - self.offset) / self.rate
        return data_send
    def recv(self,data_recv):
        self.value = data_recv * self.rate + self.offset

#定义SpnTcpMaster类，TcpMaster增加方法
class SpnTcpMaster(modbus_tk.modbus_tcp.TcpMaster):
    def __init__(self, host="127.0.0.1", port=502, timeout_in_sec=5.0):
        super().__init__(host=host, port=port, timeout_in_sec=timeout_in_sec)
        self._is_reconnect=False
        #连接状态：0-未连接；1-已连接；2-掉线；3-掉线重连
        self.connect_status=0
        self._write_buffer=[]

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

    #读单个数据
    def read(self,spn_data,slave_id=1):
        try:
            if spn_data.length == 1:
                data_format = ">h"            
            elif spn_data.length == 2:
                data_format = ">i"
            else:
                pass
            spn_data.recv(self.execute(slave_id, cst.READ_HOLDING_REGISTERS, spn_data.addr, spn_data.length,data_format=data_format)[0])
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
    #写入发送缓冲区
    def write_buffer(self,spn_data,value):
        spn_data.value=value
        self._write_buffer.append(spn_data)

    #发送写缓冲区数据
    def send_write_buffer(self,slave_id=1):
        while len(self._write_buffer) and self.is_opened():
            spn_data=self._write_buffer[0]
            try:
                self.execute(slave_id, cst.WRITE_MULTIPLE_REGISTERS, spn_data.addr,output_value=[int(spn_data.send())])
                self._write_buffer.pop(0)
                #print("写入",spn_data.name,"值：",spn_data.value)
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

    #写单个数据
    def write(self,spn_data,value,slave_id=1):
        try:
            spn_data.value=value
            self.execute(slave_id, cst.WRITE_MULTIPLE_REGISTERS, spn_data.addr,output_value=[int(spn_data.send())])
            print("写入",spn_data.name,"值：",spn_data.value)
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

    #读多个连续数据
    def read_multiple(self,addr_read_start,len_read,slave_id=1):
        try:
            recv_datas=self.execute(slave_id, cst.READ_HOLDING_REGISTERS, addr_read_start, len_read,data_format=('>'+len_read*'h'))
            #print(recv_datas)
            return recv_datas
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


#通讯矩阵
class CommunicationProtocol(object):
    def __init__(self):
        self.addr_read_start=0
        self.len_read=0
        self.attrs_readonly=[]

        self.heartbeat = SpnData(name = "heartbeat",addr = 1000,length = 1,rate = 1,offset = 0,rw="r")
        self.robot_state = SpnData(name = "robot_state",addr = 1001,length = 1,rate = 1,offset = 0,rw="r")
        self.robot_id = SpnData(name = "robot_id",addr = 1002,length = 1,rate = 1,offset = 0,rw="r")
        self.soft_version = SpnData(name = "soft_version",addr = 1003,length = 1,rate = 1,offset = 0,rw="r")
        self.robot_speed = SpnData(name = "robot_speed",addr = 1004,length = 1,rate = 1,offset = 0,rw="r")
        self.steer_angle = SpnData(name = "steer_angle",addr = 1005,length = 1,rate = 0.0573,offset = 0,rw="r")
        self.bat_voltage = SpnData(name = "bat_voltage",addr = 1006,length = 1,rate = 0.1,offset = 0,rw="r")
        self.bat_soc = SpnData(name = "bat_soc",addr = 1007,length = 1,rate = 1,offset = 0,rw="r")
        self.bat_soh = SpnData(name = "bat_soh",addr = 1008,length = 1,rate = 1,offset = 0,rw="r")
        self.water_level = SpnData(name = "water_level",addr = 1009,length = 1,rate = 1,offset = 0,rw="r")
        self.position_mark = SpnData(name = "position_mark",addr = 1010,length = 1,rate = 1,offset = 0,rw="r")
        self.position_last = SpnData(name = "position_last",addr = 1011,length = 1,rate = 1,offset = 0,rw="r")
        self.mileage_lo = SpnData(name = "mileage_lo",addr = 1012,length = 1,rate = 1,offset = 0,rw="r")
        self.mileage_hi = SpnData(name = "mileage_hi",addr = 1013,length = 1,rate = 1,offset = 0,rw="r")
        self.chassis_state = SpnData(name = "chassis_state",addr = 1014,length = 1,rate = 1,offset = 0,rw="r")
        self.arm_state = SpnData(name = "arm_state",addr = 1015,length = 1,rate = 1,offset = 0,rw="r")

        self.error_chassis_lo   = SpnData(name = "error_chassis_lo",addr = 1016,length = 1,rate = 1,offset = 0,rw="r")
        self.error_chassis_hi   = SpnData(name = "error_chassis_hi",addr = 1017,length = 1,rate = 1,offset = 0,rw="r")
        self.count_add_water   = SpnData(name = "count_add_water",addr = 1018,length = 1,rate = 1,offset = 0,rw="r")
        self.count_charged   = SpnData(name = "count_charged",addr = 1019,length = 1,rate = 1,offset = 0,rw="r")
        self.clean_state   = SpnData(name = "clean_state",addr = 1020,length = 1,rate = 1,offset = 0,rw="r")
        self.clean_time_h   = SpnData(name = "clean_time_h",addr = 1021,length = 1,rate = 1,offset = 0,rw="r")
        self.clean_time_s   = SpnData(name = "clean_time_s",addr = 1022,length = 1,rate = 1,offset = 0,rw="r")

        self.ctrl_mode = SpnData(name = "ctrl_mode",addr = 2000,length = 1,rate = 1,offset = 0,rw="rw")
        self.start_clean = SpnData(name = "start_clean",addr = 2001,length = 1,rate = 1,offset = 0,rw="rw")
        self.drive_ctrl = SpnData(name = "drive_ctrl",addr = 2002,length = 1,rate = 1,offset = 0,rw="rw")
        self.work_ctrl = SpnData(name = "work_ctrl",addr = 2003,length = 1,rate = 1,offset = 0,rw="rw")
        self.arm_ctrl = SpnData(name = "arm_ctrl",addr = 2004,length = 1,rate = 1,offset = 0,rw="rw")
        self.chassis_set = SpnData(name = "chassis_set",addr = 2005,length = 1,rate = 1,offset = 0,rw="rw")
        self.task_plan_time = SpnData(name = "task_plan_time",addr = 2006,length = 1,rate = 1,offset = 0,rw="rw")
        
        self.time_sync_rw   = SpnData(name = "time_sync_rw",addr = 2007,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_year   = SpnData(name = "time_year",addr = 2008,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_month   = SpnData(name = "time_month",addr = 2009,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_day   = SpnData(name = "time_day",addr = 2010,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_hour    = SpnData(name = "time_hour",addr = 2011,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_min    = SpnData(name = "time_min",addr = 2012,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_sec    = SpnData(name = "time_sec",addr = 2013,length = 1,rate = 1,offset = 0,rw="rw")
        self.time_weekday    = SpnData(name = "time_weekday",addr = 2014,length = 1,rate = 1,offset = 0,rw="rw")
        
        self.steer_angle_set = SpnData(name = "steer_angle_set",addr = 2015,length = 1,rate = 0.0573,offset = 0,rw="rw")
        self.robot_speed_set = SpnData(name = "robot_speed_set",addr = 2016,length = 1,rate = 1,offset = 0,rw="rw")

        
        self.get_attrs_readonly()
        self.get_addr_readonly()
        
    #获取只读数据列表
    def get_attrs_readonly(self):
        self.attrs_readonly=[]
        for attr_name in dir(self):
            attr=getattr(self,attr_name)
            if isinstance(attr,SpnData) and attr.rw=="r":
                self.attrs_readonly.append(attr)        
        return self.attrs_readonly

    #获取只读数据起始地址和长度
    def get_addr_readonly(self):
        addr_list=[]
        for attr in self.attrs_readonly:
            addr_list.append(attr.addr)
        self.addr_read_start=min(addr_list)
        self.len_read=max(addr_list)-self.addr_read_start+1        
        return self.addr_read_start,self.len_read

   
'''


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

#offset从0开始
#将某一位置为1
def set_bit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)
#将某一位清除为0
def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)
#测试某一位是否位1
def test_bit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)
#组合高低字节
def join_byte_hi_lo(hi,lo,bit_count):
    return (hi<<bit_count | lo)
'''




