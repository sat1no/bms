#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
import serial
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import RPi.GPIO as GPIO
from config import BAUDRATE, PORT


logger = modbus_tk.utils.create_logger("console")

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(26,GPIO.OUT)



def writeRegister(modul_id,rejestr, wartoscLubStan, *args, **kwargs):
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        
        master.set_timeout(0.1)
        master.set_verbose(True)
        
        GPIO.output(26,GPIO.HIGH)
        
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        master.execute(modul_id, cst.WRITE_SINGLE_REGISTER, rejestr, output_value=wartoscLubStan)
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=wartoscLubStan))
        

        GPIO.output(26,GPIO.LOW)
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        
        return -1
        
    else:
        return 1
    
def writeMultipleRegisters(modul_id,rejestr, wartoscLubStan=[], *args, **kwargs):
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        
        master.set_timeout(0.1)
        master.set_verbose(True)
        
        GPIO.output(26,GPIO.HIGH)
        
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #master.execute(modul_id, cst.WRITE_SINGLE_REGISTER, rejestr, output_value=wartoscLubStan)
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        master.execute(modul_id, cst.WRITE_MULTIPLE_REGISTERS, rejestr, output_value=wartoscLubStan)
        

        GPIO.output(26,GPIO.LOW)
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        
        return -1
        
    else:
        return 1
    
def readRegisters(modul_id,rejestr, liczbaRejestrow, *args, **kwargs):
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(0.1)
        master.set_verbose(True)
        

        dane = master.execute(modul_id, cst.READ_HOLDING_REGISTERS, rejestr, liczbaRejestrow)
        
   
    except (modbus_tk.exceptions.ModbusInvalidResponseError, modbus_tk.modbus.ModbusError) as e:
	code = ''
        if 'Response' in "%s" % e:

            code = 'Problem z komunikacją: Nieprawidłowa odpowiedź modułu'
            return code

        elif 'code' in "%s" % e:
            
            code = "Problem z komunikacją: kod błędu 2"
            return code

        return code
        
    else:
        return dane
   

if __name__ == "__main__":
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(1.0)
        master.set_verbose(True)
        logger.info("connected")
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 4))
        
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        logger.info(master.execute(52, cst.WRITE_MULTIPLE_REGISTERS, 1, output_value=[1,0,1,0]))
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
