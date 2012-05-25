import pygame
import math
import wx
from wx.glcanvas import *
from OpenGL.GL import *
import circleEvaluator

# OpenGL display code stolen from OpenGC
# http://opengc.sourceforge.net/
# Copyright (c) 2001-2004 Damion Shelton
# modified to Python by Josh Levinger

class MyHorizonIndicator(GLCanvas):
	def __init__(self,parent,id,sizeT):
		GLCanvas.__init__(self,parent,id,size=sizeT)
		#default size is (500,250)
		self.init = False
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Roll = 0
		self.Pitch = 0
		self.refresh = wx.Timer(self,id=1)
		self.refresh.Start(33) #in ms, so 30hz
		self.Bind(wx.EVT_TIMER,self.OnDraw,self.refresh)
		
	def OnEraseBackground(self, event):
		pass # Do nothing, to avoid flashing on MSW.
		
	def OnSize(self, event):
		size = self.GetClientSize()
		if self.GetContext():
			self.SetCurrent()
			glViewport(0, 0, size.width, size.height)
		event.Skip()
	
	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		self.SetCurrent()
		if not self.init:
			self.InitGL()
			self.init = True
		e = wx.PaintEvent()
		self.OnDraw(e)
	
	def InitGL(self):
		m_UnitsPerPixel = 1
		
		m_PhysicalPosition_x = 0
		m_PhysicalPosition_y = 0
		parentPhysicalPosition_x = 0
		parentPhysicalPosition_y = 0
		m_PhysicalSize_x = 94
		m_PhysicalSize_y = 98
		m_Scale_x = 1.0
		m_Scale_y = 1.0
		
		#have to cast to GLint, GLsizei explicitly with update to PyOpenGL 3.0.0a5
		#stupid, but true
		
		#The location in pixels is calculated based on the size of the
		#gauge component and the offset of the parent guage
		m_PixelPosition_x = GLsizei(int((m_PhysicalPosition_x * m_Scale_x + parentPhysicalPosition_x ) / m_UnitsPerPixel))
		m_PixelPosition_y = GLsizei(int((m_PhysicalPosition_y * m_Scale_y + parentPhysicalPosition_y ) / m_UnitsPerPixel))
		
		#The size in pixels of the gauge is the physical size / mm per pixel
		m_PixelSize_x = GLint(int(m_PhysicalSize_x / m_UnitsPerPixel * m_Scale_x))
		m_PixelSize_y = GLint(int(m_PhysicalSize_y / m_UnitsPerPixel * m_Scale_y))
		
		self.SetCurrent()
		glViewport(m_PixelPosition_x, m_PixelPosition_y, m_PixelSize_x, m_PixelSize_y)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		
		#Define the projection so that we're drawing in "real" space
		glOrtho(0, m_Scale_x * m_PhysicalSize_x, 0, m_Scale_y * m_PhysicalSize_y, -1, 1)
		#Prepare the modelview matrix
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glScalef(m_Scale_x, m_Scale_y, 1.0)
		
		
	def OnDraw(self,event):
		aCircle = circleEvaluator.CircleEvaluator()
				
		Roll = self.Roll
		Pitch = self.Pitch
		
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		
		#Move to the center of the window
		glTranslated(47,49,0)
		#Rotate based on the bank
		glRotated(Roll, 0, 0, 1)
		
		#Translate in the direction of the rotation based
		#on the pitch. On the 777, a pitch of 1 degree = 2 mm
		glTranslated(0, Pitch * -2.0, 0)
		
		#-------------------Gauge Background------------------
		#It's drawn oversize to allow for pitch and bank
		
		#The "ground" rectangle
		#Remember, the coordinate system is now centered in the gauge component
		glColor3ub(179,102,0)
		
		glBegin(GL_POLYGON)
		glVertex2f(-300,-300)
		glVertex2f(-300,0)
		glVertex2f(300,0)
		glVertex2f(300,-300)
		glVertex2f(-300,-300)
		glEnd()
		
		#The "sky" rectangle
		#Remember, the coordinate system is now centered in the gauge component
		glColor3ub(0,153,204)
		
		glBegin(GL_POLYGON)
		glVertex2f(-300,0)
		glVertex2f(-300,300)
		glVertex2f(300,300)
		glVertex2f(300,0)
		glVertex2f(-300,0)
		glEnd()
		
		#------------Draw the pitch markings--------------
		
		#Draw in white
		glColor3ub(255,255,255)
		#Specify line width
		glLineWidth(1.0)
		#The size for all pitch text
		#m_pFontManager->SetSize(m_Font,4.0, 4.0)
		
		glBegin(GL_LINES)
		
		#The dividing line between sky and ground
		glVertex2f(-100,0)
		glVertex2f(100,0)
		
		# +2.5 degrees
		glVertex2f(-5,5)
		glVertex2f(5,5)
		
		# +5.0 degrees
		glVertex2f(-10,10)
		glVertex2f(10,10)
		
		# +7.5 degrees
		glVertex2f(-5,15)
		glVertex2f(5,15)
		
		# +10.0 degrees
		glVertex2f(-20,20)
		glVertex2f(20,20)
		
		# +12.5 degrees
		glVertex2f(-5,25)
		glVertex2f(5,25)
		
		# +15.0 degrees
		glVertex2f(-10,30)
		glVertex2f(10,30)
		
		# +17.5 degrees
		glVertex2f(-5,35)
		glVertex2f(5,35)
		
		# +20.0 degrees
		glVertex2f(-20,40)
		glVertex2f(20,40)
		
		# -2.5 degrees
		glVertex2f(-5,-5)
		glVertex2f(5,-5)
		
		# -5.0 degrees
		glVertex2f(-10,-10)
		glVertex2f(10,-10)
		
		# -7.5 degrees
		glVertex2f(-5,-15)
		glVertex2f(5,-15)
		
		# -10.0 degrees
		glVertex2f(-20,-20)
		glVertex2f(20,-20)
		
		# -12.5 degrees
		glVertex2f(-5,-25)
		glVertex2f(5,-25)
		
		# -15.0 degrees
		glVertex2f(-10,-30)
		glVertex2f(10,-30)
		
		# -17.5 degrees
		glVertex2f(-5,-35)
		glVertex2f(5,-35)
		
		# -20.0 degrees
		glVertex2f(-20,-40)
		glVertex2f(20,-40)
		
		glEnd()
		
		#### +10
		###m_pFontManager->Print(-27.5,18.0,"10",m_Font)
		###m_pFontManager->Print(21.0,18.0,"10",m_Font)
		###
		#### -10
		###m_pFontManager->Print(-27.5,-22.0,"10",m_Font)
		###m_pFontManager->Print(21.0,-22.0,"10",m_Font)
		###
		#### +20
		###m_pFontManager->Print(-27.5,38.0,"20",m_Font)
		###m_pFontManager->Print(21.0,38.0,"20",m_Font)
		###
		#### -20
		###m_pFontManager->Print(-27.5,-42.0,"20",m_Font)
		###m_pFontManager->Print(21.0,-42.0,"20",m_Font)
		
		#-----The background behind the bank angle markings-------
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		
		# Draw in the sky color
		glColor3ub(0,153,204)
		
		aCircle.SetOrigin(47,49)
		aCircle.SetRadius(46)
		aCircle.SetDegreesPerPoint(5)
		aCircle.SetArcStartEnd(300.0,360.0)
		
		glBegin(GL_TRIANGLE_FAN)
		glVertex2f(0,98)
		glVertex2f(0,72)
		aCircle.Evaluate()
		glVertex2f(47,98)
		glEnd()
		
		aCircle.SetArcStartEnd(0.0,60.0)
		glBegin(GL_TRIANGLE_FAN)
		glVertex2f(94,98)
		glVertex2f(47,98)
		aCircle.Evaluate()
		glVertex2f(94,72)
		glEnd()
		
		#----------------The bank angle markings----------------
		
		# Left side bank markings
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		
		# Draw in white
		glColor3ub(255,255,255)
		
		# Move to the center of the window
		glTranslated(47,49,0)
		
		# Draw the center detent
		glBegin(GL_POLYGON)
		glVertex2f(0.0,46.0)
		glVertex2f(-2.3,49.0)
		glVertex2f(2.3,49.0)
		glVertex2f(0.0,46.0)
		glEnd()
		
		glRotated(10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,53)
		glEnd()
		
		glRotated(15.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(15.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,51)
		glEnd()
		
		# Right side bank markings
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		# Move to the center of the window
		glTranslated(47,49,0)
		
		glRotated(-10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(-10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(-10.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,53)
		glEnd()
		
		glRotated(-15.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,49)
		glEnd()
		
		glRotated(-15.0,0,0,1)
		glBegin(GL_LINES)
		glVertex2f(0,46)
		glVertex2f(0,51)
		glEnd()
		
		#----------------End Draw Bank Markings----------------
		
		
		#----------------Bank Indicator----------------
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		# Move to the center of the window
		glTranslated(47,49,0)
		# Rotate based on the bank
		glRotated(Roll, 0, 0, 1)
		
		# Draw in white
		glColor3ub(255,255,255)
		# Specify line width
		glLineWidth(2.0)
		
		glBegin(GL_LINE_LOOP) # the bottom rectangle
		glVertex2f(-4.5, 39.5)
		glVertex2f(4.5, 39.5)
		glVertex2f(4.5, 41.5)
		glVertex2f(-4.5, 41.5)
		glEnd()
		
		glBegin(GL_LINE_STRIP) # the top triangle
		glVertex2f(-4.5, 41.5)
		glVertex2f(0, 46)
		glVertex2f(4.5, 41.5)
		glEnd()
		
		#--------------End draw bank indicator------------
		
		#----------------Attitude Indicator----------------
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		# Move to the center of the window
		glTranslated(47,49,0)
		
		# The center axis indicator
		# Black background
		glColor3ub(0,0,0)
		glBegin(GL_POLYGON)
		glVertex2f(1.25,1.25)
		glVertex2f(1.25,-1.25)
		glVertex2f(-1.25,-1.25)
		glVertex2f(-1.25,1.25)
		glVertex2f(1.25,1.25)
		glEnd()
		# White lines
		glColor3ub(255,255,255)
		glLineWidth(2.0)
		glBegin(GL_LINE_LOOP)
		glVertex2f(1.25,1.25)
		glVertex2f(1.25,-1.25)
		glVertex2f(-1.25,-1.25)
		glVertex2f(-1.25,1.25)
		glEnd()
		
		# The left part
		# Black background
		glColor3ub(0,0,0)
		glBegin(GL_POLYGON)
		glVertex2f(-39,1.25)
		glVertex2f(-19,1.25)
		glVertex2f(-19,-1.25)
		glVertex2f(-39,-1.25)
		glVertex2f(-39,1.25)
		glEnd()
		glBegin(GL_POLYGON)
		glVertex2f(-19,1.25)
		glVertex2f(-19,-5.75)
		glVertex2f(-22,-5.75)
		glVertex2f(-22,1.25)
		glVertex2f(-19,1.25)
		glEnd()
		
		# White lines
		glColor3ub(255,255,255)
		glLineWidth(2.0)
		glBegin(GL_LINE_LOOP)
		glVertex2f(-39,1.25)
		glVertex2f(-19,1.25)
		glVertex2f(-19,-5.75)
		glVertex2f(-22,-5.75)
		glVertex2f(-22,-1.25)
		glVertex2f(-39,-1.25)
		glEnd()
		
		# The right part
		# Black background
		glColor3ub(0,0,0)
		glBegin(GL_POLYGON)
		glVertex2f(39,1.25)
		glVertex2f(19,1.25)
		glVertex2f(19,-1.25)
		glVertex2f(39,-1.25)
		glVertex2f(39,1.25)
		glEnd()
		glBegin(GL_POLYGON)
		glVertex2f(19,1.25)
		glVertex2f(19,-5.75)
		glVertex2f(22,-5.75)
		glVertex2f(22,1.25)
		glVertex2f(19,1.25)
		glEnd()
		
		# White lines
		glColor3ub(255,255,255)
		glLineWidth(2.0)
		glBegin(GL_LINE_LOOP)
		glVertex2f(39,1.25)
		glVertex2f(19,1.25)
		glVertex2f(19,-5.75)
		glVertex2f(22,-5.75)
		glVertex2f(22,-1.25)
		glVertex2f(39,-1.25)
		glEnd()
		#--------------End draw attitude indicator------------
		# Reset the modelview matrix
		glPopMatrix()
		glPushMatrix()
		
		aCircle.SetRadius(3.77)
		#-------------------Rounded corners------------------
		# The corners of the artificial horizon are rounded off by
		# drawing over them in black. The overlays are essentially the
		# remainder of a circle subtracted from a square, and are formed
		# by fanning out triangles from a point just off each corner
		# to an arc descrbing the curved portion of the art. horiz.
		
#		glColor3ub(0,0,0)
#		# Lower left
#		glBegin(GL_TRIANGLE_FAN)
#		glVertex2f(-1.0,-1.0)
#		aCircle.SetOrigin(3.77,3.77)
#		aCircle.SetArcStartEnd(180,270)
#		aCircle.SetDegreesPerPoint(15)
#		aCircle.Evaluate()
#		glEnd()
#		# Upper left
#		glBegin(GL_TRIANGLE_FAN)
#		glVertex2f(-1.0,99.0)
#		aCircle.SetOrigin(3.77,94.23)
#		aCircle.SetArcStartEnd(270,360)
#		aCircle.SetDegreesPerPoint(15)
#		aCircle.Evaluate()
#		glEnd()
#		# Upper right
#		glBegin(GL_TRIANGLE_FAN)
#		glVertex2f(95.0,99.0)
#		aCircle.SetOrigin(90.23,94.23)
#		aCircle.SetArcStartEnd(0,90)
#		aCircle.SetDegreesPerPoint(15)
#		aCircle.Evaluate()
#		glEnd()
#		#Lower right
#		glBegin(GL_TRIANGLE_FAN)
#		glVertex2f(95.0,-1)
#		aCircle.SetOrigin(90.23,3.77)
#		aCircle.SetArcStartEnd(90,180)
#		aCircle.SetDegreesPerPoint(15)
#		aCircle.Evaluate()
#		glEnd()
		
		# Finally, restore the modelview matrix to what we received
		glPopMatrix()
		
		glFlush()
		self.SwapBuffers()
	#end of method draw
    	
	def SetPitch(self,pitch):
		self.Pitch = pitch
		
	def SetRoll(self,roll):
		self.Roll = roll
# end of class MyHorizonIndicator