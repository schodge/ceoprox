/* -----------------------------------------------------------
Based on the sample code provided by particle.io
Shayne Hodge, 2016
---------------------------------------------------------------*/

#include "AssetTracker/AssetTracker.h"

long lastPublish = 0;
long lastBattery = 0;
int delayMinutes = 1.5 * 60 * 1000;
int delayBattery = 60 * 60 * 1000;
//int delayMinutes = 10*1000;

AssetTracker tracker = AssetTracker();
FuelGauge battery;


int gpsPublish(String command) {
    int out = 0;
    if(tracker.gpsFix()) {
        Particle.publish("G", tracker.readLatLon());
        out = 1;
    }
    return out;
}


String batteryLeft() {
        //String out =  "v:" + String::format("%.2f",battery.getVCell()) +
        //              ",c:" + String::format("%.2f",battery.getSoC());
        String out =  "c:" + String::format("%.2f",battery.getSoC());
        return out;
}


int batteryStatus(String command){
    int out = 1;
    String batt_out = batteryLeft();
    //Serial.println(batt_out);
    Particle.publish("B", batt_out);
    //out = (battery.getSoC() > 10) ? 1 : 0;
    return out;
}


void setup() {
    //Serial.begin(9600);
    //Serial.println("Turning on GPS.");
    tracker.begin();
    tracker.gpsOn();
    //Serial.println("GPS turned on (hopefully).");
    Particle.function("batt", batteryStatus);
    Particle.function("gps", gpsPublish);
}


void loop() {
    tracker.updateGPS();
    long current_time = millis();
    if(current_time-lastPublish > delayMinutes) {
        lastPublish = millis();
        //String pubAccel = String::format("%d,%d,%d", tracker.readX(),
        //                                 tracker.readY(), tracker.readZ());
        //Serial.println(pubAccel);
        //Particle.publish("A", pubAccel);
        //Serial.println(tracker.preNMEA());
        if(tracker.gpsFix()) {
            Particle.publish("G", tracker.readLatLon());
        }
        if(current_time-lastBattery > delayBattery) {
            Particle.publish("B", batteryLeft());
            lastBattery = millis();
        }
        //Serial.println(tracker.readLatLon());
    }
}
