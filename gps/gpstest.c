//Integration test of GPs nmea parse code with No.6
//Last Modified 19Sep06 jlev
 
//----- Include Files ---------------------------------------------------------
#include <avr/io.h>		// include I/O definitions (port names, pin names, etc)
#include <avr/signal.h>	// include "signal" names (interrupt names)
#include <avr/interrupt.h>	// include interrupt support
#include "uart.h"		// include uart function library
#include "rprintf.h"	// include printf function library
#include "timer.h"		// include timer function library
#include "global.h"		// include our global settings

//our nmea includes
#include "nmeap.h"
#include "nmeap_def.h"
#include "nmeap01.c"
#include "gpsmath.c"

static nmeap_context_t nmea;	//parser context
static int user_data;			//not sure what this is for...
static nmeap_gga_t     gga;     //data buffer for GGA sentences
static nmeap_rmc_t     rmc;     //data buffer for RMC sentences

static cBuffer gpsBuffer; //serial receive buffer
static char gpsBufferData[UART_RX_BUFFER_SIZE]; //allocate space in ram for buffer
void addToBuffer(unsigned char ch); //the interrupt handler

//----- Begin Code ------------------------------------------------------------
int main(void)
{
	int status;
    // Test of csik's gps math code
    struct waypoint from,to;
    //from.lat = 50.0912;
    //from.lon = -001.50;
    // set when we get valid GPS
	to.lat = 42.359051;
    to.lon = -71.093355;
	// 77 Mass Ave, taken off Google Maps
    
 	// initialize the timer system
	timerInit();
   
    //set uart receive rate to output from GPS
    uartInit();
    uartSetBaudRate(4800); //gps is 4800
   	rprintfInit(uartSendByte); //direct print output to serial
 
	// print an intro message
	rprintf("\r\nGPS TEST\r\n");
	
   	//initialize the gps receive buffer
   	bufferInit(&gpsBuffer,gpsBufferData,UART_RX_BUFFER_SIZE);

	uartSetRxHandler(addToBuffer); //custom handler	
	rprintf("set handler\r\n");
	
	//initialize gps library
	status = nmeap_init(&nmea,&user_data);
	if (status != 0) {
        rprintf("nmeap_init %d\n",status);
    }
   	// initialize gps parsers 
	status = nmeap_addParser(&nmea,"GPGGA",nmeap_gpgga,0,&gga);
	if (status != 0) {
        rprintf("nmeap_add GGA %d\n",status);
    }
    status = nmeap_addParser(&nmea,"GPRMC",nmeap_gprmc,0,&rmc);
    if (status != 0) {
        rprintf("nmeap_add RMC %d\n",status);
    }

	for(;;) {
		//make sure we have data
		char ch = bufferGetFromFront(&gpsBuffer);
		if(ch != 0) {
				//rprintf("%c",ch); //debug
				status = nmeap_parse(&nmea,ch);
				switch(status) {
					case NMEAP_GPGGA:
						rprintf("GGA");
						rprintf("\tLat: ");
						rprintfFloat(8,gga.latitude);
						rprintf(" Lon: ");
						rprintfFloat(8,gga.longitude);
						rprintf(" Alt: ");
						rprintfFloat(8,gga.altitude);
						rprintf("\r\n");
						
						//print distance to 77 Mass Ave
						from.lat = gga.latitude;
						from.lon = gga.longitude;
						rprintf("Dist to 77 (km): ");
						rprintfFloat(8,dist(from,to));
						rprintf("\r\n");
						rprintf("Bearing to 77 (deg): ");
						rprintfFloat(8,bearing(from,to));
						rprintf("\r\n\r\n");
						
						break;
					case NMEAP_GPRMC:
						rprintf("RMC");
						//rprintf("\tLat: ");
						//rprintfFloat(8,rmc.latitude);
						//rprintf(" Lon: ");
						//rprintfFloat(8,rmc.longitude);
						rprintf(" Vel (kt): ");
						rprintfFloat(8,rmc.speed);
						rprintf("\r\n");
						break;
					default:
						break;
			        } //end switch	
			
			}
	} //end for
	
	return 0;
}

void addToBuffer(unsigned char ch) {
	bufferAddToEnd(&gpsBuffer,ch);
}
