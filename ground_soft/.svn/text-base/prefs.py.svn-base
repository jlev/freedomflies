import wx
import os
import log

class PrefFrame(wx.MiniFrame):
	def __init__(self, *args, **kwds):
		wx.MiniFrame.__init__(self, *args, **kwds)
		self.parent = self.GetParent()
		mainsizer = wx.BoxSizer(wx.VERTICAL)
		portsizer = wx.FlexGridSizer(4,2)
		joysizer = wx.FlexGridSizer(6,2)
		self.radio_port_ctrl = wx.ComboBox(self,-1,'',size=(175,30))
		portsizer.Add(wx.StaticText(self,-1,"Radio Port"),0)
		portsizer.Add(self.radio_port_ctrl,1)
		portsizer.Add(wx.StaticText(self,-1,"Radio Baud"),0)
		self.radio_baud_ctrl = wx.TextCtrl(self,-1,size=(50,20))
		portsizer.Add(self.radio_baud_ctrl,1)
		ports = self.GetSerialPorts()
		for port in ports:
			self.radio_port_ctrl.Append(port)
		if len(ports) > 0:
			self.radio_port_ctrl.SetValue(ports[-1])
			
		self.joystickDict = self.ReadJoystickConfig()
		joystickList = ['']
		joystickList.extend(self.joystickDict.keys())
		joystickChoice = wx.Choice(self,-1,choices=joystickList)
		self.Bind(wx.EVT_CHOICE, self.OnJoystickChoice, joystickChoice)
		joystickChoice.SetSelection(1)
		joysizer.Add(wx.StaticText(self,-1,'Preset'),0,wx.ALIGN_LEFT)
		joysizer.Add(joystickChoice,0,wx.ALIGN_CENTER|wx.BOTTOM,border=5)
		
		joysizer.Add(wx.StaticText(self,-1,'X-Axis'),0,wx.ALIGN_LEFT)
		self.XCtrl = wx.TextCtrl(self,-1,size=(70,20))
		joysizer.Add(self.XCtrl,0,wx.ALIGN_LEFT)
		joysizer.Add(wx.StaticText(self,-1,'Y-Axis'),0,wx.ALIGN_LEFT)
		self.YCtrl = wx.TextCtrl(self,-1,size=(70,20))
		joysizer.Add(self.YCtrl,0,wx.ALIGN_LEFT)
		
		joysizer.Add(wx.StaticText(self,-1,'Throttle'),0,wx.ALIGN_LEFT)
		self.ThrottleCtrl = wx.TextCtrl(self,-1,size=(70,20))
		joysizer.Add(self.ThrottleCtrl,0,wx.ALIGN_LEFT)
		joysizer.Add(wx.StaticText(self,-1,'Dir'),0,wx.ALIGN_LEFT)
		self.ThrottleDirCtrl = wx.TextCtrl(self,-1,size=(70,20))
		joysizer.Add(self.ThrottleDirCtrl)
		
		
		joysizer.Add(wx.StaticText(self,-1,'Hat'),0,wx.ALIGN_LEFT)
		self.HatCtrl = wx.TextCtrl(self,-1,size=(140,20))
		joysizer.Add(self.HatCtrl,0,wx.ALIGN_LEFT)
		
		save_button = wx.Button(self,-1,"Apply")
		save_button.SetDefault()
		mainsizer.Add(portsizer,0,wx.LEFT|wx.TOP|wx.RIGHT,3)
		mainsizer.Add(joysizer,0,wx.LEFT|wx.TOP,3)
		mainsizer.Add(save_button,0,wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.TOP,5)
		self.SetSizer(mainsizer)
		self.Bind(wx.EVT_BUTTON,self.OnSave,save_button)
		self.Bind(wx.EVT_CLOSE,self.OnSave,save_button)
		
		#set default baud
		self.radio_baud_ctrl.SetValue("57600")

	def OnJoystickChoice(self,evt):
		try:
			data = self.joystickDict[evt.GetString()]
			self.XCtrl.SetValue(str(data['X']))
			self.YCtrl.SetValue(str(data['Y']))
			self.ThrottleCtrl.SetValue(str(data['Throttle']))
			self.ThrottleDirCtrl.SetValue(str(data['ThrottleDir']))
			self.HatCtrl.SetValue(str(data['Hat']))
		except KeyError:
			log.Log('e',"error in joystick-config.txt")
					
	def SaveJoystickChoices(self):
		xVal,yVal,tVal,hVal = 0,0,0,(-1)
			
		try:
			xVal = int(self.XCtrl.GetValue())
			yVal = int(self.YCtrl.GetValue())
			tVal = int(self.ThrottleCtrl.GetValue())
			tDirVal = eval(self.ThrottleDirCtrl.GetValue())
			hVal = eval(self.HatCtrl.GetValue()) #it's a list
		except ValueError:
			pass #no value set by user, use default
		self.parent.joystick.SetAxes(xVal,yVal,tVal,tDirVal,hVal)

	def OnSave(self,evt):
		self.SaveJoystickChoices()
		self.parent.joystickPanel.timer.Start(50) #ms
		
		radio_port = self.radio_port_ctrl.GetValue()
		radio_baud = self.radio_baud_ctrl.GetValue()
		if radio_port != "":
			self.parent.radio.radio = self.parent.radio.GetRadio(radio_port,radio_baud)

		if (self.parent.radio.radio is not None):
			#port successfully set
			self.Close() 	
	
	def GetSerialPorts(self):
		if "__WXMAC__" in wx.PlatformInfo:
			d = os.listdir('/dev')
			l = []
			for i in d:
				if (('serial' in i) or ('Serial' in i)) and ('tty' in i):
					l.append('/dev/'+i)
			return l
		else:
			pass
			#TODO: figure out what to do on other platforms
			
	def ReadJoystickConfig(self):
		try:
			f = open('joystick-config.txt','r')
			j = eval(f.read())
			return j
		except SyntaxError:
			dlg = wx.MessageDialog(self,"Syntax error in joystick-config.txt, make sure there are no empty lines or statements.","Parse error",wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
			dlg.Destroy()
			j = {'Error reading joystick-config.txt':{}}
		except IOError:
			dlg = wx.MessageDialog(self,"Cannot read joystick-config.txt","IO error",wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
			dlg.Destroy()
			j = {'Error reading joystick-config.txt':{}}
		return j