#note, cannot use log in this thread, due to non thread safe wx widgets		
	def DownlinkThread(self):
	#use ord to get integer ordinal of one character string
		while(self.downalive.isSet()):
			#input
			if self.radio is not None:
				buffer = self.radio.readline()
			else:
				print "no input"
				buffer = None		
			if buffer:
				if self.gpsout is not None:
					#make sure we have a real serial object
					self.gpsout.write(buffer)
				else:
					print buffer
				#log.Log('d',buffer) #why does this crash?
				buffer = buffer.split(',')
				kind = buffer[0]
				if kind == "$GPRMC":
					if len(buffer) != 13:
						#malformed nmea sentence
						print 'skipping',buffer
						continue
					else:
						try:
							time_acq = int(buffer[1]) #utc
							lat = buffer[3].split('.')
							lat_deg = int(lat[0][:-2])
							lat_min = int(lat[0][-2:]) + float(lat[1])/(10**len(lat[1]))
							lat_dir = buffer[4]
							lon = buffer[5].split('.')
							lon_deg = int(lon[0][:-2])
							lon_min = int(lon[0][-2:])+ float(lon[1])/(10**len(lon[1]))
							lon_dir = buffer[6]
							speed = float(buffer[7]) #knots
							course = -1*float(buffer[8]) #convert to deg CW from N
						except Exception,e:
							print e,buffer
					
					self.parent.UpdatePositionInfo(str(lat_deg),str(lat_min),str(lat_dir),
						str(lon_deg),str(lon_min),str(lon_dir))
					self.parent.UpdateAirspeed(str(speed)+' kt')
					#self.parent.compass.SetHeading(course) #weird crashes
						#why?
				if kind == "$PGRMZ":
					altitude = buffer[1] #feet
					self.parent.UpdateAltitude(str(altitude)+' ft')
				if kind == "$HCHDG":
					#only present on Garmin eTrex, Vista and GPS76S
					#magnetic value
				    heading = buffer[1]
				    deviation = buffer[2]
					#self.parent.compass.SetHeading(heading)
				if kind == "$GPRMB":
					pass
					#todo
				else:
					pass
			time.sleep(.25) #GPS signal comes in at 1hz, so no need to overdo our refresh
	#end DownlinkThread