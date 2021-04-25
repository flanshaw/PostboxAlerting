#include <ESP8266WiFi.h>
#include <PubSubClient.h>
//select LOLIN WEMOS D1 R" and mini
const char* ssid = "keepout"; // Enter your WiFi name
const char* password =  "xxx"; // Enter WiFi password
const char* mqttServer = "xxxxx;
const int mqttPort = 10140;
const char* mqttUser = "xxxxx";
const char* mqttPassword = "xxxxx";
const int ledPin =  LED_BUILTIN;
const int switchpin = 5; //D1=GPIO5
static char voltage[15];
float volt = 0;

IPAddress local_IP(192, 168, 0, xx);
IPAddress gateway(192, 168, 0, xx);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);


WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {

pinMode(ledPin,OUTPUT);
pinMode(switchpin,OUTPUT);
digitalWrite(ledPin,HIGH);
digitalWrite(switchpin,HIGH);
delay(200);
digitalWrite(ledPin, LOW);
delay(200);
digitalWrite(ledPin, HIGH);
delay(200);
digitalWrite(ledPin, LOW);
delay(200);
digitalWrite(ledPin, HIGH);
delay(200);
digitalWrite(ledPin, LOW);
delay(200);
digitalWrite(ledPin, HIGH);

Serial.begin(115200);
WiFi.config(local_IP, gateway, subnet, primaryDNS);   // not to use DHCP and faster, therefore less power  
WiFi.begin(ssid, password);
int i=0;
bool no_wifi=false;

while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    i ++;
    if (i>15){
      no_wifi = true;
      break;}
}

if (!no_wifi){
Serial.println("Connected to the WiFi network");
Serial.println(WiFi.localIP());
Serial.println(WiFi.macAddress());
Serial.println(mqttServer);
  client.setServer(mqttServer, mqttPort);
  //client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      //Serial.print("failed with state ");
      //Serial.print(client.state());
      delay(1000);
 
    }
  }
 
  client.publish("tele/postbox/open", "YES" ); //Topic name
  char str[8];
  
  //volt read doesnt work
  volt = analogRead(A0);
  dtostrf(volt,5,2,voltage);
  Serial.println(volt);
  Serial.println(voltage);
  client.publish("tele/postbox/volt", voltage); //A0 value
  //client.subscribe("esp/test");
  delay(100); // give bit of time to send before last flash then power off
digitalWrite(ledPin, LOW);
delay(500);
digitalWrite(ledPin, HIGH);
}

//turn its self off (or at least should)
Serial.println("putting switchpin to LOW, then deep sleep");
digitalWrite(switchpin,LOW);

ESP.deepSleep(0);
//need to go into deepsleep if get past this point

}
 
 
void loop() {
  client.loop();
}
