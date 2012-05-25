import wx
from bufferedcanvas import *
import cStringIO
import mapscript

debug = True
saveToDisk = False



class MapFrame(wx.Frame):
	def __init__(self,parent,id,name,pos=(50,50),size=(400,300)):
		wx.Frame.__init__(self,parent,id,name,pos,size)
		self.map = MapCanvas(self,-1,size)
		self.Bind(wx.EVT_CLOSE,self.OnClose)
		
		mit = (42.359368,-71.094208)
		self.map.setCenter(mit)
		self.map.setDist(1)
		self.map.addPlaneSymbol(mit)
		
	def OnClose(self,event):
		pass
		#don't let the user close the window, hackalicious
		
class MapCanvas(BufferedCanvas):
	def __init__(self,parent,id,size):
		wx.InitAllImageHandlers()
		self.size = size
		
		#setup map object
		self.map = mapscript.mapObj()
		self.map.width = size[0]
		self.map.height = size[1]
		#self.map.setProjection('proj=latlong,ellps=WGS84')
		self.map.setProjection('proj=lcc,ellps=GRS80') 
		# set the output format 
		self.map.setOutputFormat(mapscript.outputFormatObj('GD/PNG') )
		self.map.interlace = False #PIL can't handle interlaced PNGs
		topo=mapscript.layerObj(None) 
		topo.name="topo"  
		topo.type=mapscript.MS_LAYER_RASTER  
		topo.connectiontype=mapscript.MS_RASTER  
		topo.setProjection('proj=lcc,ellps=GRS80,datum=NAD83')
		topo.status = mapscript.MS_ON    
		topo.tileindex="maps/index.shp"
		topo.tileitem="location"
		layerNum = self.map.insertLayer(topo)
		
		#fn = self.lookupTopoFilename(0)
		#self.loadRaster(fn)
		BufferedCanvas.__init__(self,parent,id)
		
	def draw(self,dc):
		try:
			self.setDist(1)
			themap = self.map.draw()
			data = themap.saveToString()
			wx_image = wx.ImageFromStream(cStringIO.StringIO(data)) #convert to wx image
			bitmap = wx_image.ConvertToBitmap()
			if debug: print "MapServer thinks it's drawing..."
			if saveToDisk is True:
				f = open('map.png','wb')
				f.write(themap.getBytes())
				print "saving"
		except mapscript.MapServerError:
			#the map isn't ready yet
			bitmap = wx.EmptyBitmap(self.size[0],self.size[1])
			if debug: print "unable to draw, MapServerError in 'draw'."
		dc.DrawBitmap(bitmap,0,0,True)
		if debug: print "drawing"
	
	def setCenter(self,center):
		self.map.center = center
		self.update()
	
#	def lookupTopoFilename(self,point):
#		#TODO: lookup correct map name
#		#for now, just return MIT
#		return "./maps/q237898.tif"
	
	def loadRaster(self,filename):
		"""Loads raster image from filename"""

		topo=mapscript.layerObj(None) 
		topo.name="topo"  
		topo.type=MS_LAYER_RASTER  
		topo.connectiontype=MS_RASTER  
		topo.setProjection('proj=lcc,ellps=GRS80,datum=NAD83')
		topo.status = MS_ON    
		topo.tileindex="maps/index.shp"
		topo.tileitem="location"
		layerNum = self.map.insertLayer(topo)
		
		if debug:
			print "added topolayer",self.map.getLayer(layerNum).data
			print "topolayer extent",topoLayer.extent
	
	def setDist(self,dist):
		"""Create an extent for our mapObj by buffering our
		projected point by the buffer distance. Then set the mapObj's extent."""
		extent = mapscript.rectObj() 
		topleft = self.getPointFromDist(self.parent.currentLocation,dist,360-45)
		bottomright = self.getPointFromDist(self.parent.currentLocation,dist,135) #returns (lat,lon)
		
		extent.minx = min(topleft[1],bottomright[1])
		extent.miny = min(topleft[0],bottomright[0])
		extent.maxx = max(topleft[1],bottomright[1]) 
		extent.maxy = max(topleft[0],bottomright[0])
		#so it works for any quadrant
		
		self.map.setExtent(extent.minx, extent.miny, 
		               extent.maxx, extent.maxy)
		if debug: print "map extent:",self.map.extent
	
	def addPlaneSymbol(self,position):
		"""Adds the plane symbol at the indicated position"""
		pt = mapscript.pointObj()
		pt.x = position[0] #lat
		pt.y = position[1] #lon
		
		# project our point into the mapObj's projection 
		#ddproj = mapscript.projectionObj('proj=latlong,ellps=WGS84')
		#http://www.mass.gov/mgis/dd-over.htm
		ddproj = mapscript.projectionObj('proj=lcc,ellps=GRS80')
		
		origproj = mapscript.projectionObj(self.map.getProjection())
		pt.project(ddproj,origproj)
		
		# create the symbol using the image 
		planeSymbol = mapscript.symbolObj('from_img') 
		planeSymbol.type = mapscript.MS_SYMBOL_PIXMAP 
		planeImg = mapscript.imageObj('images/map-plane-small.png','GD/PNG')
		#TODO: need to rotate plane to current heading
		planeSymbol.setImage(planeImg) 
		symbol_index = self.map.symbolset.appendSymbol(planeSymbol) 

		# create a shapeObj out of our location point so we can 
		# add it to the map. 
		self.routeLine = mapscript.lineObj()
		self.routeLine.add(pt)
		routeShape=mapscript.shapeObj(mapscript.MS_SHAPE_POINT)
		routeShape.add(self.routeLine) 
		routeShape.setBounds() 

		# create our inline layer that holds our location point 
		self.planeLayer = mapscript.layerObj(None)
		self.planeLayer.addFeature(routeShape) 
		self.planeLayer.setProjection(self.map.getProjection()) 
		self.planeLayer.name = "plane" 
		self.planeLayer.type = mapscript.MS_LAYER_POINT 
		self.planeLayer.connectiontype=mapscript.MS_INLINE 
		self.planeLayer.status = mapscript.MS_ON 
		self.planeLayer.transparency = mapscript.MS_GD_ALPHA 
		
		# add the image symbol we defined above to the inline layer. 
		planeClass = mapscript.classObj(None)
		planeClass.name='plane' 
		style = mapscript.styleObj(None)
		style.symbol = self.map.symbolset.index('from_img') 
		planeClass.insertStyle(style) 
		self.planeLayer.insertClass(planeClass)
		self.map.insertLayer(self.planeLayer)
		if debug: print "added plane layer, layerorder=",self.map.getLayerOrder()
	
	def getPointFromDist(self,start,dist,brngDeg):
		"""Returns a point a specified distance [km] and bearing [deg] away from start
		From http://www.movable-type.co.uk/scripts/LatLong.html
		(c) 2002-2006 Chris Veness 
		"""
		from math import asin,sin,cos,atan2,pi,sqrt
		#convert to radians
		lat1 = start[1]*pi/180
		lon1 = start[0]*pi/180 
		brng = brngDeg*pi/180
		R = 6372.795 #Earth mean radius in km
		d = dist/R #angular distance, radians

		lat2 = asin( sin(lat1)*cos(d) + cos(lat1)*sin(d)*cos(brng) )
		lon2 = lon1 + atan2( sin(brng)*sin(d)*cos(lat1),
									cos(d)-sin(lat1)*sin(lat2) )
		return (lat2*180/pi,lon2*180/pi) #convert back to degrees
		
if __name__ == '__main__':
	app = wx.PySimpleApp()
	m = MapFrame(None,-1,"Map",size=(400,300))
	m.Show(True)	
	app.MainLoop() #don't include for iPython
	