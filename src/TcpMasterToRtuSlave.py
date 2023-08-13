#!/usr/bin/env python
"""
Pymodbus Synchronous Serial Forwarder
--------------------------------------------------------------------------

We basically set the context for the tcp serial server to be that of a
serial client! This is just an example of how clever you can be with
the data context (basically anything can become a modbus device).
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- # 
from pymodbus.server.sync import StartTcpServer as StartServer
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from pymodbus.datastore.remote import RemoteSlaveContext
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.version import version

# --------------------------------------------------------------------------- # 
# project imports
# --------------------------------------------------------------------------- # 
import ConfigHandler

# --------------------------------------------------------------------------- # 
# importing TcpMaster and RtuSlave Data
# --------------------------------------------------------------------------- # 
Mode = ConfigHandler.InitConfigs()
# Slave here means RtuSlave
TcpMasterIP = str((Mode["Slave"])["TcpMasterIP"]) 
TcpMasterPort = int((Mode["Slave"])["TcpPort"])
RtuPortForGateway = str((Mode["Slave"])["RtuPort"])
PeerID = int((Mode["Slave"])["PeerID"])
Timeout = int((Mode["Slave"])["Timeout"])
Baudrate = int((Mode["Slave"])["Baudrate"]) 

# --------------------------------------------------------------------------- # 
# configure the service logging
# --------------------------------------------------------------------------- # 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = version.short()

def run_serial_forwarder():
    # ----------------------------------------------------------------------- #
    # initialize the datastore(serial client)
    # Note this would send the requests on the serial client with address = 0

    # ----------------------------------------------------------------------- #
    client = ModbusClient(method='rtu', port=RtuPortForGateway,baudrate=Baudrate,timeout=Timeout) # Rtu Client of RtuSlave
    # If required to communicate with a specified client use unit=<unit_id>
    # in RemoteSlaveContext
    # For e.g to forward the requests to slave with unit address 1 use
    # store = RemoteSlaveContext(client, unit=1)
    store = RemoteSlaveContext(client,unit= PeerID)
    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # run TcpMaster <-> RtuSlave Server
    # ----------------------------------------------------------------------- #
    StartServer(context,identity=identity address=(TcpMasterIP, TcpMasterPort)) # Tcp Server of TcpMaster


if __name__ == "__main__":
    run_serial_forwarder()