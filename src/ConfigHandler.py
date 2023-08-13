#!/usr/bin/env python
#
#  @functions: InitConfigs(), ReadConfigs(), CreateJsonFile(), UpdateConfigs()
#  @created on: 15/05/22
#  This module is used to Read and Update Configurations of the Gateway (Direction of Dataflow) saved in config.json
#

# standard imports
import json
import jmespath

# project imports


def InitConfigs():
    try:
       mode = ReadConfigs()
       return mode # Return Read Data in json format

    except:
        file_configs = open("config.json", 'w', encoding = 'utf-8')
        # perform write operation

        json_var = CreateJsonFile()
        
        file_configs.write(json_var)
        file_configs.close()
        
        mode = ReadConfigs()
        return mode


# Reads the config.json file and returns a python-json object (equivalent obj)
def ReadConfigs():

    file_configs = open("config.json", 'r', encoding = 'utf-8')
    # perform read operation
    data = file_configs.read()
    json_obj = json.loads(data)


    #RTUSLAVE
    RtuSlave = jmespath.search("mode.RtuSlave", json_obj) # Returns object RtuSlave in python Data type dict in this case

    #RTUMASTER
    RtuMaster = jmespath.search("mode.RtuMaster", json_obj) # Returns object RtuMaster in python Data type dict in this case
    

    file_configs.close()
    Mode={"Master":RtuMaster, "Slave":RtuSlave}
    return Mode



# Modularised to use in InitConfigs()
def CreateJsonFile():

    json_var = '''{
            "mode": {
                "RtuSlave": {
                    "TcpMasterIP": "127.0.0.1",
                    "TcpPort": 0,
                    "RtuPort": "/dev/tty5", 
                    "PeerID": 0,
                    "Timeout": 0,
                    "Baudrate": 9600,
                    "FrameBreak": 0
                },

                "RtuMaster": {
                    "TcpSlaveIP": "127.0.0.1",
                    "TcpPort" : 502,
                    "RtuPort": "/dev/tty5"
                    "PeerID": 0,
                    "Timeout": 0,
                    "Baudrate": 9600,
                    "FrameBreak": 0
                }
            }
        }'''
    
    return json_var


# Updating config.json to desired configurations for Rtu Master/Slave mode 
def UpdateConfigs(Mode, IP, ID, Port, Timeout, Baudrate, FrameBreak):
    # perform update operation
    Data = None
    Data = ReadConfigs()
    if Mode == "RtuSlave":
        
        json_var = '''{
            "mode": {
                "RtuSlave": {
                    "TcpMasterIP": "'''+str(IP)+'''",
                    "PeerID": '''+str(ID)+''',
                    "TcpPort": '''+str(TcpPort)+''',
                    "RtuPort": '''+str(RtuPort)+''',
                    "Timeout": '''+str(Timeout)+''',
                    "Baudrate": '''+str(Baudrate)+''',
                    "FrameBreak": '''+str(FrameBreak)+'''
                },

                "RtuMaster": {
                    "TcpSlaveIP": "'''+str(Data['Master']['TcpSlaveIP'])+'''",
                    "PeerID": '''+str(Data['Master']['PeerID'])+''',
                    "TcpPort": '''+str(Data['Master']['TcpPort'])+''',
                    "RtuPort": '''+str(Data['Master']['RtuPort'])+''',
                    "Timeout": '''+str(Data['Master']['Timeout'])+''',
                    "Baudrate": '''+str(Data['Master']['Baudrate'])+''',
                    "FrameBreak": '''+str(Data['Master']['FrameBreak'])+'''
                }
            }
        }'''

        #print(json_var)

        file_configs = open("config.json", 'w', encoding = 'utf-8')
        file_configs.write(json_var)
        file_configs.close()
        

    elif Mode == "RtuMaster":
        
        json_var = '''{
            "mode": {
                "RtuSlave": {
                    "TcpMasterIP": "'''+str(Data['Slave']['TcpMasterIP'])+'''",
                    "PeerID": '''+str(Data['Slave']['PeerID'])+''',
                    "TcpPort": '''+str(Data['Slave']['TcpPort'])+''',
                    "RtuPort": '''+str(Data['Master']['RtuPort'])+''',
                    "Timeout": '''+str(Data['Slave']['Timeout'])+''',
                    "Baudrate": '''+str(Data['Slave']['Baudrate'])+''',
                    "FrameBreak": '''+str(Data['Slave']['FrameBreak'])+'''
                },

                "RtuMaster": {
                    "TcpSlaveIP": "'''+str(IP)+'''",
                    "PeerID": '''+str(ID)+''',
                    "TcpPort": '''+str(TcpPort)+''',
                    "RtuPort": '''+str(RtuPort)+''',
                    "Timeout": '''+str(Timeout)+''',
                    "Baudrate": '''+str(Baudrate)+''',
                    "FrameBreak": '''+str(FrameBreak)+'''
                }
            }
        }'''
        
        file_configs = open("config.json", 'w', encoding = 'utf-8')
        file_configs.write(json_var)
        file_configs.close()