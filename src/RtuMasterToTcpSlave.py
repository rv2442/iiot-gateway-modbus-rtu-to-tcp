#!/usr/bin/env python
"""
Pymodbus Synchronous Tcp Forwarder
--------------------------------------------------------------------------

We basically set the context for the serial server to be that of a
tcp client! This is just an example of how clever you can be with
the data context (basically anything can become a modbus device).
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- # 
from pymodbus.server.sync import StartSerialServer as StartServer
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from pymodbus.datastore.remote import RemoteSlaveContext
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.version import version

# --------------------------------------------------------------------------- # 
# project imports
# --------------------------------------------------------------------------- # 
import ConfigHandler

# --------------------------------------------------------------------------- # 
# importing TcpSlave and RtuMaster Data
# --------------------------------------------------------------------------- # 
Mode = ConfigHandler.InitConfigs()
# Master here means RtuMaster
TcpSlaveIP = str((Mode["Master"])["TcpSlaveIP"])
TcpSlavePort = int((Mode["Master"])["TcpPort"])
RtuPortForGateway = str((Mode["Master"])["RtuPort"])
PeerID = int((Mode["Master"])["PeerID"])
Timeout = int((Mode["Master"])["Timeout"])
Baudrate = int((Mode["Master"])["Baudrate"]) 

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

def run_tcp_forwarder():
    # ----------------------------------------------------------------------- #
    # initialize the datastore(serial client)
    # Note this would send the requests on the serial client with address = 0

    # ----------------------------------------------------------------------- #
    client = ModbusClient(TcpSlaveIP,port=TcpSlavePort,timeout=Timeout) # Tcp Client of TcpSlave
    # If required to communicate with a specified client use unit=<unit_id>
    # in RemoteSlaveContext
    # For e.g to forward the requests to slave with unit address 1 use
    # store = RemoteSlaveContext(client, unit=1)
    store = RemoteSlaveContext(client,unit=PeerID)
    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # run a RtuMaster <-> TcpSlave Server
    # ----------------------------------------------------------------------- #
    StartServer(context,identity=identity,framer=ModbusRtuFramer,port=RtuPortForGateway,baudrate=Baudrate) # Rtu Server of RtuMaster


if __name__ == "__main__":
    run_tcp_forwarder()