#include <gpsmath.h>


double dist(struct waypoint from, struct waypoint to){
    double a, delta_lat, delta_lon;

    from.lat = from.lat* M_PI / 180;
    to.lat = to.lat*M_PI/180;
    from.lon = from.lon*M_PI/180;
    to.lon = to.lon*M_PI/180;
    
    delta_lat = to.lat - from.lat;
    delta_lon = to.lon - from.lon;
    
    a = sin(delta_lat/2) * sin(delta_lat/2) + cos(from.lat) * cos(to.lat) * sin(delta_lon/2) * sin(delta_lon/2);
    a = 2 * atan2(sqrt(a), sqrt(1-a));
    a = R * a;
    
    return a; //in km
}

double bearing(struct waypoint from, struct waypoint to){
    double a,b;
    
    from.lat = from.lat* M_PI / 180;
    to.lat = to.lat*M_PI/180;
    from.lon = from.lon*M_PI/180;
    to.lon = to.lon*M_PI/180;
    
    a = sin(to.lon - from.lon)*cos(to.lat);
    b = cos(from.lat)*sin(to.lat) - sin(from.lat)*cos(to.lat)*cos(to.lon-from.lon);
    a = atan2(a,b)*180/M_PI;
    
    return a; //in degrees
}

