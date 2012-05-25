import wx
from bufferedcanvas import *
import math


class MyCompass(BufferedCanvas):
	def __init__(self,parent,id,sizeT):
		#get bitmaps before init
		wx.InitAllImageHandlers()
		self.plane_img = wx.Image('images/compass-plane.png', wx.BITMAP_TYPE_PNG)
		self.plane = wx.BitmapFromImage(self.plane_img,-1)
		BufferedCanvas.__init__(self,parent,id,size=sizeT)
		self.SetHeading(0) #start pointed at north
		#default size is (200,200)
		
	def draw(self,dc):
		try:
			theta = self.heading
		except AttributeError:
			#not init'ed yet
			self.heading = math.pi/2 #start at north
			theta = self.heading
		#draw background
		dc.SetBrush(wx.WHITE_BRUSH)
		dc.DrawRectangle(0,0,200,200)
		
		#draw compass rose
		dc.SetBrush(wx.LIGHT_GREY_BRUSH)
		dc.DrawCircle(100,100,95)
		dc.SetBrush(wx.WHITE_BRUSH)
		dc.DrawCircle(100,100,85)
		
		#draw info
		origin = wx.Point(100,100)
		r_x = math.cos(theta)
		r_y = math.sin(theta)
		
		#draw lines at 45 degree intervals
		black = wx.Pen("black",5,wx.SOLID)
		dc.SetPen(black)
		theta_deg = int(theta*180/math.pi)
		for angle in range(theta_deg,theta_deg + 360,45):
			angle_rad = angle*math.pi/180
			r_x = math.cos(angle_rad)
			r_y = math.sin(angle_rad)
			start = wx.Point(int(r_x*80),int(r_y*80)) + origin
			end = wx.Point(int(r_x*95),int(r_y*95)) + origin
			dc.DrawLine(start.x,start.y,end.x,end.y)
			
		#draw north
		theta = self.heading
		r_x = math.cos(theta)
		r_y = math.sin(theta)
		red = wx.Pen("red",5,wx.SOLID)
		dc.SetPen(red)
		north_start = wx.Point(int(r_x*80),int(r_y*80)) + origin
		north_end = wx.Point(int(r_x*95),int(r_y*95)) + origin
		dc.DrawLine(north_start.x,north_start.y,north_end.x,north_end.y)

		#draw direction labels
		label_font = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
		dc.SetFont(label_font)
		dc.SetTextForeground(wx.BLACK)
		dc.SetTextBackground(wx.WHITE)
		(r_x,r_y) = (math.cos(theta),math.sin(theta))
		(x_size,y_size) = dc.GetTextExtent("N")
		text_left_corner = wx.Point(int(r_x*70-x_size/2),int(r_y*70)-y_size/2) + origin
		dc.DrawText("N",text_left_corner.x,text_left_corner.y)
		(r_x,r_y) = (math.cos(theta+math.pi/2),math.sin(theta+math.pi/2))
		(x_size,y_size) = dc.GetTextExtent("E")
		text_left_corner = wx.Point(int(r_x*70-x_size/2),int(r_y*70)-y_size/2) + origin
		dc.DrawText("E",text_left_corner.x,text_left_corner.y)
		(r_x,r_y) = (math.cos(theta+math.pi),math.sin(theta+math.pi))
		(x_size,y_size) = dc.GetTextExtent("S")
		text_left_corner = wx.Point(int(r_x*70-x_size/2),int(r_y*70)-y_size/2) + origin
		dc.DrawText("S",text_left_corner.x,text_left_corner.y)
		(r_x,r_y) = (math.cos(theta+3*math.pi/2),math.sin(theta+3*math.pi/2))
		(x_size,y_size) = dc.GetTextExtent("W")
		text_left_corner = wx.Point(int(r_x*70-x_size/2),int(r_y*70)-y_size/2) + origin
		dc.DrawText("W",text_left_corner.x,text_left_corner.y)
		
		#draw plane
		dc.DrawBitmap(self.plane,0,0,True)
	#end draw method
	def SetHeading(self,heading):
		#heading entered as degrees from horiz, +CW
		self.heading = heading * math.pi/180 - math.pi/2 #rad from vert, +CW
		self.update()
#end of class MyCompass