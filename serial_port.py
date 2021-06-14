#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'serial port class'

__author__ = 'cc'

import sys
import serial
import serial.tools.list_ports
import binascii
import logging
import threading
from time import sleep

serial_tool_title = '''
**** Serial tool v0.0 used for command line ****
**** press' + SQ +'to exit or '+ SR+'refresh com port ****
'''
MENU_EXIT = 'SQ'
MENU_REFRESH = 'SR'
COM_PREFIX = 'COM'

userInput=None
userInputSemphore = threading.Semaphore()
menuSemphore = threading.Semaphore()

menLock = threading.Semaphore()

def serialUserReadInput():
	global userInput
	while True:
		userInput = raw_input()
		userInputSemphore.release()


class Serial_port(object):
	"""docstring for serial_port"""
	def __init__(self, port=None, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
		timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None):
		self.port = port
		self.baudrate = baudrate
		self.bytesize = bytesize
		self.parity = parity
		self.stopbits = stopbits
		self.timeout = timeout
		self.xonxoff = xonxoff
		self.rtscts = rtscts
		self.write_timeout = write_timeout
		self.dsrdtr = dsrdtr
		self.inter_byte_timeout = inter_byte_timeout
		self.device = None
		self.recvData = ''
		self.alive = False
		self.port_list={}
		# print self.port
		# print self.baudrate
		# print self.bytesize
		# print self.parity
		# print self.stopbits
		# print self.xonxoff
		# print self.rtscts
		# print self.dsrdtr

	def serialport_list(self):
		ports = list(serial.tools.list_ports.comports())
		if len(ports) <= 0:
			return None
		for x in ports:
			self.port_list[str(list(x)[0])]= str(list(x)[1])

		return self.port_list

	def serialport_open(self, port, baudrate=115200):
		if self.alive:
			self.serialport_close()
		if port == None or port.upper() not in self.port_list.keys():
			return False
		self.device = serial.Serial()
		self.device.port = port.upper()
		self.device.baudrate = baudrate
		self.device.bytesize = self.bytesize
		self.device.parity = self.parity
		self.device.stopbits = self.stopbits
		self.device.timeout = self.timeout
		self.device.xonxoff = self.xonxoff
		self.device.rtscts = self.rtscts
		self.device.write_timeout = self.write_timeout
		self.device.dsrdtr = self.dsrdtr
		self.device.inter_byte_timeout = self.inter_byte_timeout
		try:
			self.device.open()
			if self.device.isOpen():
				self.alive = True
				return True
		except IOError as e:
			self.alive = False
			logging.error(e)
			return False
		
	def serialport_close(self):
		if self.device.isOpen():
			self.alive = False			
			self.device.close()

	def serialport_read(self):
		while True:
			#print 'test'
			if self.alive:
				try:
					number = self.device.inWaiting()
					if number:
						#print(self.device.read(number), end='')
						#print self.device.read(number),
						sys.stdout.write(self.device.read(number))
						sys.stdout.flush()
					# if self.recvData != '':
					# 	for x in self.recvData.splitlines(True):
					# 		if '\n' in x:
					# 			self.recvData=self.recvData.replace(x,'')
					# 			print x
				except IOError as e:
					logging.error(e)

	def serialport_write(self, data):
		if self.alive:
			#print 'written data '
			# if isHex:
			# 	data = binascii.unhexlify(data)
			self.device.write(data)
			self.device.flush()
			#self.device.reset_output_buffer()

def displayMenu(port):
	port_list=port.serialport_list()
	if port_list != None:
		print('select port form list(PORT:115200):\r')
		for key, value in port_list.items():
			print str(key+' - '+ value + '\r\n')
	else:
		print 'no COM port available'

def processMenuCommand():
	global userInput
	global serialport
	global serialRead
	global serialUserInput

	displayMenu(serialport)
	portbaudrate = 115200
	portindex=''
	while True:
		#print 'menu'
		userInputSemphore.acquire()
		#print 'got'
		#print userInput
		if COM_PREFIX in userInput.upper():
			if ':' in userInput:
				portbaudrate=int(userInput.split(':')[1])
				portindex=userInput.split(':')[0]
			else:
				portindex=userInput
				portbaudrate = 115200
			if serialport.serialport_open(port = portindex, baudrate=portbaudrate) == False:
				print 'Invalid input, please retry'
				continue
			else:
				print '**** '+portindex.upper() +':'+ str(portbaudrate) + ' open successfully'+' ****'
		elif userInput.upper() == MENU_EXIT:
			#stop_thread(serialRead)
			#stop_thread(serialUserInput)
			return
		elif userInput.upper() == MENU_REFRESH:
			displayMenu(serialport)
			continue
		else:
			if userInput == '':
				userInput = '\n'
			if len(bytearray(userInput)) > 1:
				userInput=userInput+'\n'
			serialport.serialport_write(bytearray(userInput))
			continue

if __name__ == '__main__':

	global serialport
	global serialRead
	global serialUserInput

	print serial_tool_title

	userInputSemphore.acquire()

	serialport=Serial_port()

	serialUserInput = threading.Thread(target = serialUserReadInput)
	serialMenu = threading.Thread(target = processMenuCommand)
	#serialRead.join()

	serialRead = threading.Thread(target = serialport.serialport_read)
	serialRead.setDaemon(True)
	serialRead.start()

	serialUserInput.setDaemon(True)
	serialUserInput.start()
	#serialUserInput.join()

	serialMenu.setDaemon(True)
	serialMenu.start()
	serialMenu.join()

