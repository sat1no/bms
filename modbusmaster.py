#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python
 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr
 This is distributed under GNU LGPL license, see license.txt
"""

import sys
import serial

#add logging capability
import logging

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu


# logger = modbus_tk.utils.create_logger("console")





def writeRegister(modul_id,rejestr, wartoscLubStan, *args, **kwargs):
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port='/dev/ttyAMA0', baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(1.0)
        master.set_verbose(True)
        
        
        
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        master.execute(modul_id, cst.WRITE_SINGLE_REGISTER, rejestr, output_value=wartoscLubStan)
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        
        return -1
        
    else:
        return 1
    
def readRegisters(modul_id,rejestr, liczbaRejestrow, *args, **kwargs):
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port='/dev/ttyAMA0', baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(1.0)
        master.set_verbose(True)
        
        
        
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        a = master.execute(modul_id, cst.READ_HOLDING_REGISTERS, rejestr, liczbaRejestrow)
        
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        # logger.info(a)
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(modul_id, cst.WRITE_SINGLE_REGISTER, rejestr, output_value=wartoscLubStan))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        
        return -1
    else:
        return a
   

if __name__ == "__main__":
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port='/dev/ttyAMA0', baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(1.0)
        master.set_verbose(True)
        logger.info("connected")
        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        
        #send some queries
        logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
