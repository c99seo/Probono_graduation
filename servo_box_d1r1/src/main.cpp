// #include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

const char* ssid = "iptime";
const char* password = "cwseo5489";
const char* mqtt_server = "3.19.148.223";  // EC2 인스턴스의 공인 IP 주소
// const char* topic = "servo";

Servo servo;

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  // Serial.println("New message received:");
  for (unsigned int i = 0; i < length; i++) {
    // Serial.print((char)payload[i]);
    message += (char)payload[i]; 
  }

  if(strcmp(topic, "rasp/open") == 0) {
    int angle = message.toInt();  // 받은 메시지 정수 변환
    if(angle >= 0 && angle <= 180){
      servo.write(angle);
      Serial.println(angle);
    }
  }
  else if(strcmp(topic, "rasp/close") == 0){
    int angle = message.toInt();
    if(angle >= 0 && angle <= 180){
      servo.write(angle);
      Serial.println(angle);
    }
  }
}

void setup(){
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  

  while (!client.connected()) {
    if (client.connect("arduino-subscriber")) {
      Serial.println("Connected");
      client.subscribe("rasp/open");
      client.subscribe("rasp/close");
    } else {
      delay(1000);
    }
  }

  servo.attach(D2);
}

void loop(){
  client.loop();
 
}

// 90도 -> open
// 180도 -> close