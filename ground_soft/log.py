import wx
from bufferedcanvas import *
import os,time

import mutex

def SetGlobals(err,dl,ul):
	global error,downlink,uplink
	error = err
	downlink = dl
	uplink = ul

#global log accessor function
def Log(id,message):
	global error,downlink,uplink
	if id == 'e':
		error.mutex.lock(error.DoLogString,message)
	if id == 'd':
		downlink.mutex.lock(downlink.DoLogString,message)
	if id == 'u':
		uplink.mutex.lock(uplink.DoLogString,message)
	
class MyLog(wx.PyLog):
	"Class to allow real time logging of uplink/download/interface events"
	def __init__(self, name, notebook):
		wx.PyLog.__init__(self)
		self.tc = wx.TextCtrl(notebook, -1, style = wx.TE_MULTILINE|wx.TE_READONLY)
		self.logTime = True
		self.mutex = mutex.mutex() #control access to text controls
		self.name = name
		try:
			os.mkdir('logs')
		except OSError:
			#directory already exists
			pass
			
		self.filename = 'logs/'+time.strftime("%Y%m%d-%H%M")+self.name+'.txt'
		self.logfile_opened = False
		#logfile opened in button in main
		
		
	def OpenLogFile(self):
		if not self.logfile_opened:
			self.outfile = open(self.filename,'w')
			self.logfile_opened = True
			
	def CloseLogFile(self):
		self.outfile.flush()
		self.outfile.close()
		self.logfile_opened = False
	
	def DoLogString(self, message):
		#write to text control
		#WX GUI ISN'T THREAD SAFE!
		#self.tc.AppendText(message + '\n')
		#self.tc.ShowPosition(self.tc.GetNumberOfLines()) #scroll to bottom		
		#only add time to stdout and logfile, not enough space in text control
		if self.logTime:
				message = time.strftime("%X", time.localtime()) + ": " + message
		if self.logfile_opened:
			self.outfile.write(message + '\n')
			self.outfile.flush()
		else:
			if self.name is "downlink":
				print "d",message[:-1] #strip \r\n
			if self.name is "error":
				print "e",message
			if self.name is "uplink":
				print "u",message
		self.mutex.unlock()
#end of class MyLog