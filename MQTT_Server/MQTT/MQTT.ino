#include <WiFi.h>
#include <PubSubClient.h>

#define ledPin 2
int temp_val = 0;
long lastMsg = 0;
const char *ssid = "WE_D28CA0";
const char *password = "31097022";
const char *mqtt_server = "192.168.1.138";

volatile int counter = 0;  // عدد النبضات من الإنكودر
volatile int current_position = 0;
const int pulses_per_revolution = 360;  // عدد النبضات لكل دورة كاملة - يجب تعديل هذا بناءً على إنكودرك

int R_PWM = 32;  // قطب PWM للموتور اليمين
int L_PWM = 33;  // قطب PWM للموتور اليسار

int R_EN = 25;  // تغيير تعريف R_EN ليكون على القطب رقم 5
int L_EN = 26;  // قطب تمكين الموتور اليسار
#define low1 34
#define low2 35

const int freq = 5000;
const int ledChannel = 0;
const int ledChannel1 = 1;
const int resolution = 8;


WiFiClient espClient;
PubSubClient client(espClient);


void moveMotor(int angle) {

  int error = angle - counter;
  while (error) {
    error = angle - counter;
    if (error > 5)  // تحريك يمين
    {
      ledcWrite(ledChannel1, 0);
      ledcWrite(ledChannel, 80);

    } else if (error < -5)  // تحريك يسار
    {
      ledcWrite(ledChannel1, 80);
      ledcWrite(ledChannel, 0);
    } else {
      error = 0;
      ledcWrite(ledChannel, 0);
      ledcWrite(ledChannel1, 0);
    }
  }
}

void ai0() {

  if (digitalRead(12) == LOW) {  //CCW
    current_position--;
    counter--;
  } else  //CW
  {
    current_position++;
    counter++;
  }
}

float mapFloat(float value, float in_min, float in_max, float out_min, float out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


void setup_wifi() {
  delay(50);
  //Serial.println();
  //Serial.print("Connecting to ");
  //Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);  //
    //Serial.print(".");
  }

  //Serial.println("");
  //Serial.println("WiFi connected");
  //Serial.println("IP address: ");
  //Serial.println(WiFi.localIP());
}

void connect_mqttServer() {
  // Loop until we're reconnected
  while (!client.connected()) {
    // first check if connected to wifi
    if (WiFi.status() != WL_CONNECTED) {
      // if not connected, then first connect to wifi
      setup_wifi();
    }
    // now attemt to connect to MQTT server
    //Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_client")) {
      // attempt successful
      //Serial.println("connected");

      // Subscribe to topics here
      client.subscribe("esp32/data");
      client.subscribe("esp32/angle");
      client.subscribe("esp32/sms_state");
      client.subscribe("esp32/state");
      client.subscribe("esp32/CarSteer");
      client.publish("esp32/state", "1");
    } else {
      // attempt not successful
      //Serial.print("failed, rc=");
      //Serial.print(client.state());
      //Serial.println(" trying again in 2 seconds");
      delay(2000);
    }
  }
}

// this function will be executed whenever there is data available on subscribed topics
void callback(char *topic, byte *message, unsigned int length) {
  //Serial.print("Message arrived on topic: ");
  //Serial.print(topic);
  //Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    //Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  //Serial.println();

  // Check if a message is received on the topic
  if (String(topic) == "esp32/sms_state") {
    if (messageTemp == "1") {
      //Serial.println("=======================");
      //Serial.println("Action: Driver Sleep");
      //Serial.println("Action: Turn On buzzer");
      //Serial.println("=======================");
      digitalWrite(ledPin, HIGH);
    }

    if (messageTemp == "0") {
      //Serial.println("=======================");
      //Serial.println("Action: Driver Awake");
      //Serial.println("=======================");
      digitalWrite(ledPin, LOW);
    }
  }

  if (String(topic) == "esp32/CarSteer") {
    float x = messageTemp.toFloat();
    float y = mapFloat(x, -1.0, 1.0, -180.0, 180.0);
    int y_int = (int)y;
    if (temp_val!= y_int) {

        //Serial.println("====================");
        //Serial.println(y_int);
        temp_val = y_int;
        moveMotor(y_int);
        //Serial.println("====================");
      }
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(low1, OUTPUT);
  pinMode(low2, OUTPUT);
  digitalWrite(low1, LOW);
  digitalWrite(low2, LOW);


  ledcSetup(ledChannel, freq, resolution);
  ledcSetup(ledChannel1, freq, resolution);

  // attach the channel to the GPIO to be controlled
  ledcAttachPin(R_PWM, ledChannel);
  ledcAttachPin(L_PWM, ledChannel1);

  pinMode(R_EN, OUTPUT);  // تعيين R_EN كمخرج
  pinMode(L_EN, OUTPUT);  // تعيين L_EN كمخرج

  digitalWrite(R_EN, HIGH);  // تفعيل الموتور اليمين
  digitalWrite(L_EN, HIGH);  // تفعيل الموتور اليسار

  pinMode(12, INPUT_PULLUP);  // تفعيل المقاومة الداخلية للسحب لأعلى للرقم 2
  pinMode(13, INPUT_PULLUP);  // تفعيل المقاومة الداخلية للسحب لأعلى للرقم 3



  // attachInterrupt(digitalPinToInterrupt(2), ai0, FALLING);  // تفعيل الانقطاع عند تغيير الإشارة
  attachInterrupt(13, ai0, FALLING);  // تفعيل الانقطاع عند تغيير الإشارة

  //Serial.begin(115200);
  setup_wifi();



  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    connect_mqttServer();
  }
  client.loop();
  long now = millis();
  // if (now - lastMsg > 4000) {
  //   lastMsg = now;
  //   //topic name (to which this ESP32 publishes its data). 37 is the dummy value.
  //   client.publish("esp32/angle", "37");
  // }
}