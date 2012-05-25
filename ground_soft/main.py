#!/usr/bin/env pythonw
"""Licensed under the MIT License
***
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
***
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
***
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#main imports
import time
import math
import sys,os
import threading

#my imports
import prefs
import joystick as joystickClass #avoid name collision
import compass
import horizon
import log
import map
from bufferedcanvas import *
import datalink
from pyTS import TerraImage

#temporary configuration settings
#TODO make this a pickleable, readable config file
class configuration(object):
	def __init__(self, name):
		self.name = name
		print self.name
	def set_map(map):
		self.map = map

theConfig = configuration("generic")
theConfig.map = False


#external library imports
try:
	import wx
	import wx.glcanvas
except ImportError:
	print "cannot import wx"
	sys.quit()
	
try:
	import pygame
except ImportError:
	print "cannot import pygame"
	sys.quit()

try:
	import serial
except ImportError:
	print "cannot import pyserial"
	sys.quit()


class AppFrame(wx.Frame):
	def __init__(self,*args,**kwds):
		wx.Frame.__init__(self,*args,**kwds)
		
		#init pygame first, may take awhile
		pygame.init()
		
		#top sizer elements
		self.airspeed_gauge = wx.Gauge(self, -1, 100, size=(20,400), style=wx.GA_VERTICAL|wx.GA_SMOOTH)
		self.altitude_gauge = wx.Gauge(self, -1, 100, size=(20,400), style=wx.GA_VERTICAL|wx.GA_SMOOTH)
		self.horizon = horizon.MyHorizonIndicator(self,-1,(500,500)) #sizes here are wrong, but it needs to be this way
		
		#force initial paint of OGL, mega-kludge
		tempPaintEvent = wx.PaintEvent()
		self.horizon.OnPaint(tempPaintEvent)
		self.horizon.SetClientSize((400,400)) #proper size
		del tempPaintEvent
		
		self.airspeed_value = wx.TextCtrl(self,-1,size=(50,20),style=wx.TE_READONLY)
		self.altitude_value = wx.TextCtrl(self,-1,size=(50,20),style=wx.TE_READONLY)
	
		#bottom sizer elements
		button_width = (80,20)
		self.autopilot_button = wx.ToggleButton(self, -1, "Autopilot",size=button_width)
		self.engine_button = wx.ToggleButton(self, -1, "Engine",size=button_width)
		self.logfile_button = wx.ToggleButton(self, -1, "Log to file",size=button_width)
		self.radio_button = wx.ToggleButton(self, -1, "Radio",size=button_width)
		
		self.notebook = wx.Notebook(self, -1, size = (350,125), style=0)
		self.error_log = log.MyLog('error',self.notebook)
		self.downlink_log = log.MyLog('downlink',self.notebook)
		self.uplink_log = log.MyLog('uplink',self.notebook)
		self.notebook.AddPage(self.error_log.tc, "Error")
		self.notebook.AddPage(self.downlink_log.tc, "Downlink")
		self.notebook.AddPage(self.uplink_log.tc, "Uplink")
		log.SetGlobals(self.error_log,self.downlink_log,self.uplink_log)
		#pass these objects to log class
		
		self.lat_ctrl = wx.TextCtrl(self, -1,size=(80,20),style=wx.TE_READONLY|wx.TE_RICH2)
		self.lat_dir_text = wx.StaticText(self, -1, " ")
		self.lon_ctrl = wx.TextCtrl(self, -1,size=(80,20),style=wx.TE_READONLY|wx.TE_RICH2)
		self.lon_dir_text = wx.StaticText(self, -1, " ")
		self.gps_error_ctrl = wx.TextCtrl(self, -1,size=(80,20),style=wx.TE_READONLY|wx.TE_RICH2)
		self.throttle_gauge = wx.Gauge(self, -1, 10,size=(100,20),style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
		
		
		#right sizer elements
		self.joystick = joystickClass.Joystick()
		self.joystickPanel = joystickClass.JoyPanel(self)
		self.compass = compass.MyCompass(self,-1,(250,250)) #use old compass (not OGL)
		#self.compass = heading.MyHeadingIndicator(self,-1,(500,500))
		
		#start sizer layout
		main_sizer = wx.BoxSizer(wx.VERTICAL) #the big kahuna
		top_sizer = wx.BoxSizer(wx.HORIZONTAL) #holds horizon and right sizers
		horizon_sizer = wx.BoxSizer(wx.HORIZONTAL) #holds horizon, alt and speed
		right_sizer = wx.BoxSizer(wx.VERTICAL) #holds joystick, radio checks
		bottom_sizer = wx.FlexGridSizer(1, 3,hgap=5) #holds buttons, logs, text display
		
		airspeed_sizer = wx.BoxSizer(wx.HORIZONTAL)
		altitude_sizer = wx.BoxSizer(wx.HORIZONTAL)
		airspeed_sizer.Add(self.airspeed_value,0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT,3)
		airspeed_sizer.Add(self.airspeed_gauge,0,wx.RIGHT,-2)
		altitude_sizer.Add(self.altitude_gauge,0,wx.LEFT,5)
		altitude_sizer.Add(self.altitude_value,0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT,0)
		horizon_sizer.Add(airspeed_sizer, 0)
		horizon_sizer.Add(self.horizon, 0)
		horizon_sizer.Add(altitude_sizer, 0)
		
		right_sizer.Add(self.compass,0,wx.CENTER)
		right_sizer.Add(self.joystickPanel,0,wx.RIGHT)

		top_sizer.Add(horizon_sizer,0,wx.RIGHT,5)
		top_sizer.Add(right_sizer,0,wx.LEFT,0)
		main_sizer.Add(top_sizer,0,wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT,3)
		
		button_sizer = wx.GridSizer(2, 2, vgap=5,hgap=5)
		button_sizer.Add(self.radio_button, 0)
		button_sizer.Add(self.autopilot_button, 0)
		button_sizer.Add(self.logfile_button, 0)
		button_sizer.Add(self.engine_button, 0)
		bottom_sizer.Add(button_sizer,0,wx.LEFT|wx.ALIGN_CENTER_VERTICAL,5)
		self.Bind(wx.EVT_TOGGLEBUTTON,self.OnRadioButton,self.radio_button)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.OnLogToFile,self.logfile_button)
		
		info_sizer = wx.FlexGridSizer(4,2,vgap=5)
		lat_sizer = wx.BoxSizer(wx.HORIZONTAL)
		info_sizer.Add(wx.StaticText(self, -1, "Latitude"),1)
		lat_sizer.Add(self.lat_dir_text,0,wx.RIGHT,7)
		lat_sizer.Add(self.lat_ctrl,0,wx.RIGHT,5)
		info_sizer.Add(lat_sizer,0,wx.ALIGN_LEFT,0)
		lon_sizer = wx.BoxSizer(wx.HORIZONTAL)
		info_sizer.Add(wx.StaticText(self, -1, "Longitude"),1)
		lon_sizer.Add(self.lon_dir_text,0,wx.RIGHT,7)
		lon_sizer.Add(self.lon_ctrl,0,wx.RIGHT,5)
		info_sizer.Add(lon_sizer,0,wx.ALIGN_LEFT,0)
		
		info_sizer.Add(wx.StaticText(self, -1, "Accuracy"),1)
		info_sizer.Add(self.gps_error_ctrl)
		info_sizer.Add(wx.StaticText(self, -1, "Throttle"),1)
		info_sizer.Add(self.throttle_gauge)
		bottom_sizer.Add(self.notebook,1)
		bottom_sizer.Add(info_sizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT)
		
		main_sizer.Add(bottom_sizer,0)
		self.SetAutoLayout(True)
		self.SetSizer(main_sizer)
		self.Layout()
		self.SetMinSize((800,600))
		#end of main window items
		
		#Menubar
		self.MenuBar = wx.MenuBar()
		FileMenu = wx.Menu()
		#
		#hack
		about = FileMenu.Append(-1, 'About FreedomFlies')
		self.Bind(wx.EVT_MENU,self.OnAbout,about)
		#
		FileMenu.AppendSeparator()
		prefs = FileMenu.Append(-1,'Preferences')
		quit = FileMenu.Append(-1, "E&xit\tAlt-X", "Exit")
		self.Bind(wx.EVT_MENU,self.OnQuit,quit)
		self.MenuBar.Append(FileMenu, '&File')

		#TODO: figure out how to do help menu right on Macs
		#HelpMenu = wx.Menu()
		#about = HelpMenu.Append(-1, 'About FreedomFlies')
		#self.Bind(wx.EVT_MENU,self.OnAbout,about)
		self.Bind(wx.EVT_MENU,self.OnPrefs,prefs)
		#if "__WXMAC__" in wx.PlatformInfo: 
		#	wx.App.SetMacAboutMenuItemId(about.GetId())
		#	wx.App_SetMacHelpMenuTitleName("&Help")
		#else:
		#	self.MenuBar.Append(HelpMenu, "&Help")
			
		SetupMenu = wx.Menu()
		#cal = SetupMenu.Append(-1,'Calibrate Joystick')
		#self.Bind(wx.EVT_MENU,self.OnJoystickCalibrate,cal)
		gtest = SetupMenu.Append(-1,"Graphics Test")
		self.Bind(wx.EVT_MENU,self.OnGraphicsTest,gtest)
		if(theConfig.map):
			map = SetupMenu.Append(-1,"Map")
			self.Bind(wx.EVT_MENU,self.OnMap,map)
		self.MenuBar.Append(SetupMenu,"Setup")
		self.SetMenuBar(self.MenuBar)
		#end of menubar
		
		# flags for main	
		self.gpsout_port = ""
		self.radio_port = ""
		#init radio, set for real by prefs dialog
		self.radio = datalink.radiolink(self,self.radio_port,self.gpsout_port)
	#end __init__
		
	def OnQuit(self, event):
		self.radio.StopUplinkThread()
		self.radio.StopDownlinkThread()
		self.Close()
		time.sleep(1) #to allow the threads to really close
		pygame.quit()
		sys.exit()
		
	def OnAbout(self, event):
		info = wx.AboutDialogInfo()
		info.SetName('Freedom Flies')
		info.SetVersion('0.1')
		info.SetDescription('An Open-Source UAV')
		info.AddDeveloper('Chris Csikszentmihalyi')
		info.AddDeveloper('Jorge de la Garza')
		info.AddDeveloper('Josh Levinger')
		info.AddDeveloper('Ryan Luerson')
		info.SetLicence(__doc__)
		info.SetCopyright("Copyright (C) 2005-2007 MIT Media Lab")
		info.SetWebSite('http://freedomflies.berlios.de')
		wx.AboutBox(info)
	
		
	def OnMap(self,event):
		if (theConfig.map):
			self.parent.map.Show()
	
	def OnPrefs(self,event):
		self.parent.prefs.Show()
		
	def OnGraphicsTest(self,event):
		max_pitch = 30
		max_roll = 75
		incr = 1
		sleep_time = 0.01 #sec
	
		for i in range(0,max_pitch,incr):
			self.horizon.SetPitch(i)
			time.sleep(sleep_time)
			wx.Yield()
		for i in range(max_pitch,-max_pitch,-incr):
			self.horizon.SetPitch(i)
			time.sleep(sleep_time)
			wx.Yield()
		for i in range(-max_pitch,0,incr):
			self.horizon.SetPitch(i)
			time.sleep(sleep_time)
			wx.Yield()
			
		self.horizon.SetPitch(0)
		self.horizon.SetRoll(0)
			
		for i in range(0,max_roll,incr):
			self.horizon.SetRoll(i)
			time.sleep(sleep_time)
			wx.Yield()
		for i in range(max_roll,-max_roll,-incr):
			self.horizon.SetRoll(i)
			time.sleep(sleep_time)
			wx.Yield()
		for i in range(-max_roll,0,incr):
			self.horizon.SetRoll(i)	
			time.sleep(sleep_time)
			wx.Yield()
			
		self.horizon.SetPitch(0)
		self.horizon.SetRoll(0)
			
		for i in range(0,361,2):
			self.compass.SetHeading(i)
			wx.Yield()
		
	def OnRadioButton(self,event):
		btn = event.GetEventObject()
		if btn.GetValue() == True:
			self.radio.StartUplinkThread()
			self.radio.StartDownlinkThread()
		if btn.GetValue() == False:
			self.radio.StopUplinkThread()
			self.radio.StopDownlinkThread()
	
	def OnLogToFile(self,event):
		btn = event.GetEventObject()
		if btn.GetValue() == True:
			print "opening logfile, all further messages will go there"		
			self.error_log.OpenLogFile()
			self.downlink_log.OpenLogFile()
			self.uplink_log.OpenLogFile()
		if btn.GetValue() == False:
			print "closing logfile, all further messages will go to stdout"	
			self.error_log.CloseLogFile()
			self.downlink_log.CloseLogFile()
			self.uplink_log.CloseLogFile()
					
	def UpdateLatitude(self,lat_deg,lat_dir):
		if lat_dir is ("+" or "W"):
			dirVal = 1
		if lat_dir is ("-" or "E"):
			dirVal = -1
		self.currentLocation.Lat = dirVal*lat_deg
		
		if (theConfig.map):
			self.parent.map.map.setCenter(self.currentLocation)
		self.lat_ctrl.SetValue(str(lat_deg))
		self.lat_dir_text.SetLabel(lat_dir)
		
	def UpdateLongitude(self,lon_deg,lon_dir):	
		if lon_dir is ("+" or "N"):
			dirVal = 1
		if lon_dir is ("-" or "S"):
			dirVal = -1
		self.currentLocation.Lon = dirVal*lon_deg
		if (theConfig.map):
			self.parent.map.map.setCenter(self.currentLocation)
		self.lon_ctrl.SetValue(str(lon_deg))
		self.lon_dir_text.SetLabel(lon_dir)
	def UpdateAltitude(self,alt):
		self.altitude_value.SetValue(alt)
	def UpdateAirspeed(self,v):
		self.airspeed_value.SetValue(v)
# end of class AppFrame

class MyApp(wx.App):
	def OnInit(self):
		wx.InitAllImageHandlers()
		self.mainWin = AppFrame(None, 1, "Freedom Flies",(50,25),(800,600))
		self.mainWin.parent = self #just for link in OnMap and OnPrefs
		self.mainWin.currentLocation = TerraImage.point(42.35830436,-71.09108681) #start location is MIT
		if (theConfig.map):
			self.map = map.MapFrame(self.mainWin,-1,"Map",(855,25),(400,400))
		self.prefs = prefs.PrefFrame(self.mainWin,-1,"Preferences",(855,425),(300,225))
		self.mainWin.Show()
		if (theConfig.map):
			self.map.Show()
		self.prefs.Show()
		self.SetTopWindow(self.mainWin)
		self.Bind(wx.EVT_CLOSE,self.mainWin.OnQuit)
		return True
# end of class MyApp

if __name__ == "__main__":
	app = MyApp(0)
	try:
		app.MainLoop()
		#fake move event so horizon settles properly, but doesn't work
		TempMoveEvent = wx.MoveEvent(pos=(50,50),winid=1)
		TempMoveEvent.ResumePropagation(1)
		del TempMoveEvent
	finally:
		pygame.quit()