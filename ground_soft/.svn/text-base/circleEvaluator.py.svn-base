from math import pi,sin,cos
from OpenGL.GL import *

class CircleEvaluator:
	# this coded stolen from OpenGC
	# http://opengc.sourceforge.net/
	# Copyright (c) 2001-2004 Damion Shelton
	
	def __init__(self):
		self.m_XOrigin = 0;
		self.m_YOrigin = 0;
		self.m_StartArcDegrees = 0;
		self.m_EndArcDegrees = 0;
		self.m_DegreesPerPoint = 10;		
		self.m_Radius = 1;
		
	def SetOrigin(self,x,y):
		self.m_XOrigin = x
		self.m_YOrigin = y
		
	def SetArcStartEnd(self,startArc, endArc):
		self.m_StartArcDegrees = startArc
		self.m_EndArcDegrees = endArc
	
	def SetDegreesPerPoint(self,degreesPerPoint):
		self.m_DegreesPerPoint = degreesPerPoint

	def SetRadius(self,radius):
		if (radius > 0):
			self.m_Radius = radius
		else:
			self.m_Radius = 1
	
	def Evaluate(self):
		#We parametrically evaluate the circle
		#x = sin(t)
		#y = cos(t)
		#t goes from 0 to 2pi
		#0 degrees = 0rad, 90 degrees = pi/2rad, etc.
	
		startRad = self.m_StartArcDegrees / 180.0 * pi
		endRad = self.m_EndArcDegrees / 180.0 * pi
		radPerPoint = self.m_DegreesPerPoint / 180.0 * pi
		
		if (startRad > endRad):
			endRad += 2*pi
			
		currentRad = startRad
		
		while(currentRad < endRad):
			x = self.m_Radius*sin(currentRad) + self.m_XOrigin
			y = self.m_Radius*cos(currentRad) + self.m_YOrigin
			glVertex2d(x,y)
			currentRad += radPerPoint
		
		x = self.m_Radius*sin(endRad) + self.m_XOrigin
		y = self.m_Radius*cos(endRad) + self.m_YOrigin
		glVertex2d(x,y)
