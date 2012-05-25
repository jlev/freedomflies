"""A script to load compiled code to the #6 microcontroller.
Requires pyserial.
Usage: nosixloader.py --port=[port] --baud --file=[file.hex]
jlev 6Apr2007
"""
import serial
import sys
import time
import optparse

def main():
	parser = optparse.OptionParser()
	parser.add_option("-p", "--port",
		action="store", type="string", dest="portname",default=0,
		help="the serial port")
	parser.add_option("-f", "--file",
		action="store", type="string", dest="filename",
		help="the .hex file to be loaded")
	parser.add_option("-b", "--baud",
		action="store", type="int", dest="baudrate", default=57600,
		help="the baud rate")
	parser.add_option("-l", "--linedelay",
		action="store", type="int", dest="linedelay", default=1,
		help="line delay, in 60ths of a second")
	(options, args) = parser.parse_args()

	if (options.filename is None):
		print "--file required"
		return 2 
	if (options.portname is None):
		print "no port specified, trying first available"
		return 2
	try:
		port = serial.Serial(options.portname,options.baudrate,
			timeout=1,bytesize=8,stopbits=1,parity='N',writeTimeout=1)
		port.open()
	except serial.SerialException,e:
		print "Serial Exception:",e
		return 2

	#ensure 6 is there
	port.write("This is a test. Testing 123.\r\n")
	time.sleep(.1)
	buffer = port.readlines()
	
	if "Syntax error\r\n" not in buffer:
		print "#6 not connected, or is not in bootload mode"
		return 3
	else:
		print "connected to #6"
	
	hexfile = open(options.filename,'r')
	lines = hexfile.readlines()
	print "writing",options.filename,"to #6"
	
	i = 0
	for l in lines:
		try:	
			w = l[:-2] + '\n' #get newlines right
			port.write(w)
			print repr(w) #show
			i=i+1
			time.sleep(options.linedelay/60.0)
		except serial.serialutil.SerialTimeoutException:
			print "write timeout on line",i
			port.close()
			return -1
			
	buffer = port.read(100)
	print buffer
	
	port.close()
	
if __name__ == "__main__":
	sys.exit(main())