from mapscript import *   
map=mapObj() 
map.width = 600 
map.height = 600 

map.setProjection('proj=lcc,ellps=GRS80') 
map.setOutputFormat(outputFormatObj('GD/PNG')) 
topo=layerObj(None) 
topo.name="topo"  
topo.type=MS_LAYER_RASTER  
topo.connectiontype=MS_RASTER  
#topo.data="./maps/237898.jp2"  
topo.setProjection('proj=lcc,ellps=GRS80,datum=NAD83')
topo.status = MS_ON    
topo.tileindex="./index.shp"
topo.tileitem="location"
layerNum = map.insertLayer(topo) 
map.setExtent(233001,897999,236822,901998)
#map.setExtent(327000, 4691000, 328000, 4692000)
jim = map.draw()
jim.save("okay.png")


#MAP
#	SIZE 1200 800
#	EXTENT  33000.000000 24015.601562 547080.775610 962000.219008
#	LAYER
#		NAME "topos"
#		STATUS ON
#		TILEINDEX "index.shp"
#		TILEITEM "location"
#		TYPE RASTER
#	END
#	LAYER
#		NAME stuff
#		TYPE POLYGON
#		STATUS DEFAULT
#		DATA index.shp
#		CLASS
#			STYLE
#				OUTLINECOLOR 100 100 100
#			END
#		END
#	END
#END





# Mapping calls, using Mapscript and gdal

# 1. start with a folder full of geotiffs.  Run gdaltindex index.shp q*.tif*      
# index.shp is the shape file, with elements
# index.dbf has the file names, ostensibly in the same order as the elements
# TODO: Figure out some of the field info




                            
from mapscript import *
shpfile = shapefileObj('index.shp') 
shpfile.numshapes
shp = shpfile.getShape(shpfile.numshapes-1)  
shp.getArea() 
tilerect=shp.bounds
tilerect.maxx
tilerect.minx
tilerect.maxy
tilerect.miny
#put it together with:
#shp2img -m test.map -o test.png -e 154000 886000 158000 890000                     

#ALL BELOW was simply to experiment!  Not necessary.
f = open("index.dbf", "rb")             
fileList=f.readlines()
f.close()
fileList = fileList[0]
#Originally had to use '   '.'' but switched 3space and '' with two space and ' ' -- anyway, play around\n
fileList = fileList.replace('   ',' ')
fileList = fileList.replace('  ','') 
fileList = fileList.split(' ')
fileList.pop(0)
fileList[shpfile.numshapes-1]

MIT = pointObj(42.35830436,-71.09108681) 
shp.contains(MIT)

for theShp in range(shpfile.numshapes):
	if shpfile.getShape(theShp).contains(MIT):
		# print fileList(theShp)
		print "!!!!"
	else:
		print '.'



