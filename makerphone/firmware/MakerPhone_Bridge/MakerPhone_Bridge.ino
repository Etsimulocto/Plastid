#include <Arduino.h>
// MakerPhone USB bring-up v0.1.0. No GPIO or peripherals driven.
char line[384]; size_t used=0; unsigned long last=0;
void hello(){Serial.println("{\"type\":\"hello\",\"board\":\"esp32s3\",\"fw\":\"0.1.0\",\"project\":\"MakerPhone\",\"protocol\":1}");}
void status(){Serial.printf("{\"type\":\"status\",\"component\":\"controller\",\"state\":\"ready\",\"uptime_ms\":%lu}\n",millis());}
void command(const char* s){
if(strstr(s,"\"hello\""))hello();
else if(strstr(s,"\"diag.run\""))Serial.println("{\"type\":\"diag\",\"component\":\"usb_serial\",\"state\":\"pass\"}");
else if(strstr(s,"\"modem.status\""))Serial.println("{\"type\":\"status\",\"component\":\"modem\",\"state\":\"unverified\"}");
else if(strstr(s,"\"status\""))status();
else Serial.println("{\"type\":\"error\",\"code\":\"unsupported\"}");
}
void setup(){Serial.begin(115200);delay(1000);hello();status();}
void loop(){while(Serial.available()){char c=Serial.read();if(c=='\n'){line[used]=0;if(used)command(line);used=0;}else if(c!='\r'){if(used<sizeof(line)-1)line[used++]=c;else used=0;}}if(millis()-last>=5000){last=millis();status();}delay(2);}
