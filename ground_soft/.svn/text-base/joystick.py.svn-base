#!/usr/bin/pythonw
# joystick.py

import wx
import pygame
import log

class JoyPanel(wx.Panel):
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)
		self.timer = wx.Timer(self, 1)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		#parent's already got the joystick
		self.joystick = parent.joystick
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.control = JoyGauge(self,self.joystick)
		self.throttle_pos = wx.Gauge(self, -1,100,size=(100,20),style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
		self.throttle_dir_text = wx.StaticText(self, -1, " ")
		#self.CalibratedButton = wx.Button(self,-1,"Calibrated")
		sizer.Add(self.control,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
		throttle_sizer = wx.BoxSizer(wx.HORIZONTAL)
		throttle_sizer.Add(self.throttle_pos,0,wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT,5)
		throttle_sizer.Add(self.throttle_dir_text,0,wx.ALIGN_RIGHT)
		sizer.Add(throttle_sizer,wx.ALIGN_CENTER_HORIZONTAL)
		#sizer.Add(self.text,1,wx.ALIGN_CENTER)
		#sizer.Add(self.CalibratedButton,1,wx.ALIGN_CENTER)
		#self.Bind(wx.EVT_BUTTON,self.OnCalibrated,self.CalibratedButton)
		#self.CalibratedButton.SetDefault()
		
		self.SetSizer(sizer)
		#self.SetMinSize((200,300))
		#self.SetAutoLayout(True)
		#self.Layout()
		
		#self.timer.Start(50) #every 50 ms, or 20hz
		#start timer in OnSave in prefs.py
		x,y = self.joystick.getPos()
	#end method __init__
	
	def OnTimer(self, event):
		pygame.event.pump()
		try:
			x,y = self.joystick.getPos()
			self.control.Update(x,y)
			
			throttle = self.joystick.getThrottle()
			self.throttle_pos.SetValue(abs(throttle))
			dir = "X"
			if throttle < 0:
				dir = "R"
			if throttle > 0:
				dir = "F"
			self.throttle_dir_text.SetLabel(dir)
		except pygame.error:
			#user already notified in Joystick.SetAxes
			pass
	
	def OnClose(self, event):
		self.timer.Stop()
		#self.Close()

class Joystick(object):
	def __init__(self,*args,**kwds):
		try:
			self.stick = pygame.joystick.Joystick(0)
			status = self.stick.init() #returns none
			if(status == None):
				pass
			#	 log.Log('e',"joystick successfully initialized")
			else:
				log.Log('e',"could not initialize joystick, status " + str(status))
		except pygame.error,err:
			log.Log('e',str(err))
			self.stick = None
	
	def SetAxes(self,X,Y,T,TD,H):
		self.XNum = X
		self.YNum = Y
		self.ThrottleNum = T
		self.ThrottleDir = TD
		self.HatNum = H
		try:
			testX = self.stick.get_axis(self.XNum)
		except pygame.error:
			log.Log('e',"Invalid Joystick X-Axis Setting")
			self.XNum = -1
			
		try:
			testY = self.stick.get_axis(self.YNum)
		except pygame.error:
			log.Log('e',"Invalid Joystick Y-Axis Setting")
			self.YNum = -1
			
		try:
			testThrottle = self.stick.get_axis(self.ThrottleNum)
		except pygame.error:
			log.Log('e',"Invalid Joystick Throttle Setting")
			self.ThrottleNum = -1
				
		try:
			testThrottleR = self.stick.get_button(int(self.ThrottleDir[0]))
		except pygame.error:
			log.Log('e','Invalid Throttle Direction List')
			self.ThrottleDir[0] = -1
		try:
			testThrottleF = self.stick.get_button(int(self.ThrottleDir[1]))
		except pygame.error:
			#log.Log('e','Invalid Throttle Button Forward')
			self.ThrottleDir[1] = -1
		
		try:
			if len(H) > 1:
				try:
					#it's a series of buttons
					testHat0 = self.stick.get_button(int(self.HatNum[0]))
					testHat1 = self.stick.get_button(int(self.HatNum[1]))
					testHat2 = self.stick.get_button(int(self.HatNum[2]))
					testHat3 = self.stick.get_button(int(self.HatNum[3]))
				except pygame.error:
					log.Log('e',"Invalid Joystick Hatswitch Button List")
					self.HatNum = -1
		except TypeError:
			#it's a real hatswitch
			try:
				testHat = self.stick.get_hat(self.HatNum)
			except pygame.error:
				log.Log('e',"Invalid Joystick Hatswitch Setting")
				self.HatNum = -1
	
	def getPos(self):
		"ranges 0-100"
		try:
			raw_x = self.stick.get_axis(self.XNum)
			raw_y = self.stick.get_axis(self.YNum)
		except AttributeError:
			raw_x,raw_y = 0,0 #incorrect values
		except NameError:
			log.Log('e',"joystick axes not set")
		
		x = int(raw_x * 100)
		y = int(raw_y * -100)
		return x,y
		
	def getButton(self,buttonNum):
		return self.stick.get_button(buttonNum)
	
	def getHat(self):
		raw_x,raw_y = 0,0 #init
		try:
			if len(self.HatNum) > 1:
				#it's a list of buttons, build the hat ourselves
				raw_north = self.stick.get_button(self.HatNum[0])
				raw_east = self.stick.get_button(self.HatNum[1])
				raw_south = self.stick.get_button(self.HatNum[2])
				raw_west = self.stick.get_button(self.HatNum[3])
				#convert to x,y
				raw_x = raw_east - raw_west
				raw_y = raw_north - raw_south
		except TypeError:
			#it's a real hatswitch
			raw_x,raw_y = self.stick.get_hat(self.HatNum)
		except NameError:
			log.Log('e','joystick hat not set')
		return raw_x,raw_y
		
	def getThrottle(self):
		"ranges 0-100"
		try:
			dir = 0
			try:
				R = self.stick.get_button(self.ThrottleDir[0])
			except pygame.error:
				R = 0
			try:
				F = self.stick.get_button(self.ThrottleDir[1])
			except pygame.error:
				#button doesn't exist, pretend it is pressed
				#so default action is forward, unless reverse is pressed
				F = 1
				
			if (F is 1):
				dir = 1
			if (R is 1):
				dir = -1

			raw_pos = self.stick.get_axis(self.ThrottleNum)
			throttle = dir*float(((raw_pos-1)*50) +3) #should range (0,100)
			
		except AttributeError:
			log.Log('e',"could not access throttle")
			throttle = 0
		except NameError,e:
			log.Log('e',"joystick axes not set")
			throttle = 0
		return throttle

class JoyGauge(wx.Panel):
	#shamelessly stolen from the wxPython Demo, but using pygame for joystick
    def __init__(self, parent, stick):
        
        self.stick = stick
        size = (150,150)
        
        wx.Panel.__init__(self, parent, -1, size=size)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        
        self.buffer = wx.EmptyBitmap(*size)
        dc = wx.BufferedDC(None, self.buffer)
        self.DrawFace(dc)
        self.DrawJoystick(dc,0,0)
    
    def OnSize(self, event):
        # The face Bitmap init is done here, to make sure the buffer is always
        # the same size as the Window
        w, h  = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w,h)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.DrawFace(dc)
        self.DrawJoystick(dc,0,0)

    
    def DrawFace(self, dc):
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

    
    def OnPaint(self, evt):
        # When dc is destroyed it will blit self.buffer to the window,
        # since no other drawing is needed we'll just return and let it
        # do it's thing
        dc = wx.BufferedPaintDC(self, self.buffer)

    
    def DrawJoystick(self, dc,joyx,joyy):
        # draw the gauge as a maxed square in the center of this window.
        w, h = self.GetClientSize()
        edgeSize = min(w, h)
        
        xorigin = (w - edgeSize) / 2
        yorigin = (h - edgeSize) / 2
        center = edgeSize / 2
        
        # Restrict our drawing activities to the square defined
        # above.
        dc.SetClippingRegion(xorigin, yorigin, edgeSize, edgeSize)
        
        # Optimize drawing a bit (for Win)
        dc.BeginDrawing()
        
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawRectangle(xorigin, yorigin, edgeSize, edgeSize)
        
        dc.SetPen(wx.Pen(wx.BLACK, 1, wx.DOT_DASH))
        
        dc.DrawLine(xorigin, yorigin + center, xorigin + edgeSize, yorigin + center)
        dc.DrawLine(xorigin + center, yorigin, xorigin + center, yorigin + edgeSize)
        
        if self.stick:
            # Get the joystick position as a float
            #joyx,joyy passed in from above
            
            #Get the joystick range of motion
            xmin = -100 #self.stick.GetXMin()
            xmax = 100 #self.stick.GetXMax()
            if xmin < 0:
                xmax += abs(xmin)
                joyx += abs(xmin)
                xmin = 0
            xrange = max(xmax - xmin, 1)
            
            ymin = -100 #self.stick.GetYMin()
            ymax = 100 #self.stick.GetYMax()
            if ymin < 0:
                ymax += abs(ymin)
                joyy += abs(ymin)
                ymin = 0
            yrange = max(ymax - ymin, 1)
            
            # calc a ratio of our range versus the joystick range
            xratio = float(edgeSize) / xrange
            yratio = float(edgeSize) / yrange
            
            # calc the displayable value based on position times ratio
            xval = int(joyx * xratio)
            yval = int(joyy * yratio)
            
            # and normalize the value from our brush's origin
            x = xval + xorigin
            y = yval + yorigin
            
            # Now to draw it.
            dc.SetPen(wx.Pen(wx.RED, 2))
            dc.CrossHair(x, y)
        
        # Turn off drawing optimization
        dc.EndDrawing()
    
    def Update(self,x,y):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.DrawFace(dc)
        self.DrawJoystick(dc,x,y)