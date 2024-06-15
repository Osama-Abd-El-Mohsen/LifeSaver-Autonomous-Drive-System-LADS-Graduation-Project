#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Encoder.h>
/*************************************************************
******************** Define Network Config *******************
*************************************************************/
// const char *ssid = "WE_D28CA0";
// const char *ssid = "Mi 11 Lite";
// const char *password = "00000000";
// const char *mqtt_server = "192.168.50.97";  // RPI ip
const char *ssid = "WE_D28CA0";
const char *password = "31097022";
const char *mqtt_server = "192.168.1.138";  // RPI ip

int prev_steer_angle = 0;
/*************************************************************
************************* define pins ************************
*************************************************************/
#define Buzzer_pin 2
/****************************************************************/
#define CLK 13  // CLK ENCODER
#define DT 15   // DT ENCODER

/****************************************************************/
#define RPWM 32
#define R_EN 25
#define R_IS 34

#define LPWM 33  // define pin 6 for LPWM pin (output)
#define L_EN 26  // define pin 7 for L_EN pin (input)
#define L_IS 35  // define pin 8 for L_IS pin (output)
/****************************************************************/


/*************************************************************
******************* define const variables *******************
************************** for PWM ***************************
*************************************************************/
int target_angle = 0;
int counter = 0;
int speed = 0;
int direction = 0;
int steer_angle_int = 0;
long previousTime = 0;
float ePrevious = 0;
float eIntegral = 0;

const int freq = 5000;
const int PWM_channel0 = 0;
const int PWM_channel1 = 1;
const int resolution = 8;

WiFiClient espClient;
PubSubClient client(espClient);
ESP32Encoder encoder;

/*************************************************************
********** Function to move motor to specific angle **********
*************************************************************/
void moveMotor(int angle) {
  // int state = 2;
  // while (state != 0) {
  //   Serial.println("in while");
  counter = encoder.getCount() / 2;

  speed = fabs(pidController(angle, 0.002, 0.002, 0.002));
  if (speed < 40) {
    speed = 40;
  } 
  else if (speed > 50) {
    speed = 50;
  }

  if (direction == -1) {
    motor_moveCW(speed);
    // state = 1;
  } 
  else if (direction == 1) {
    motor_moveCCW(speed);
    // state = 1;
  } 
  else if (direction == 0) {
    motor_stop();
    // state = 0;
  }
  // }
}


void motor_moveCW(int speed) {
  if (speed > 255) {
    speed = 255;
  }

  digitalWrite(R_EN, HIGH);
  ledcWrite(PWM_channel0, speed);

  digitalWrite(L_EN, HIGH);
  ledcWrite(PWM_channel1, 0);
}

void motor_moveCCW(int speed) {
  if (speed > 255) {
    speed = 255;
  }

  digitalWrite(R_EN, HIGH);
  ledcWrite(PWM_channel0, 0);

  digitalWrite(L_EN, HIGH);
  ledcWrite(PWM_channel1, speed);
}

void motor_stop() {
  digitalWrite(R_EN, LOW);
  ledcWrite(PWM_channel0, 0);

  digitalWrite(L_EN, LOW);
  ledcWrite(PWM_channel1, 0);
}

float pidController(int target, float kp, float ki, float kd) {
  //Measure time elapsed since the last iteration
  long currentTime = micros();
  float deltaT = ((float)(currentTime - previousTime)) / 1.0e6;

  //Compute the error, derivative, and integral
  int e = target - counter;
  float eDerivative = (e - ePrevious) / deltaT;
  eIntegral = eIntegral + e * deltaT;

  if (e > 0) {
    direction = 1;
  } else if (e < 0) {
    direction = -1;

  } else if (e == 0) {
    direction = 0;
  }

  //Compute the PID control signal
  float u = (kp * e) + (kd * eDerivative) + (ki * eIntegral);

  //Update variables for the next iteration
  previousTime = currentTime;
  ePrevious = e;

  return u;
}

/*************************************************************
********************** Map Float value Func ******************
**************************************************************/
float mapFloat(float value, float in_min, float in_max, float out_min, float out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


/*************************************************************
************************* Wifi Setup *************************
**************************************************************/
void setup_wifi() {
  delay(50);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);  //
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


/*************************************************************
***************** Connecting to MQTT Broker ******************
**************************************************************/
void connect_mqttServer() {
  // Loop until we're reconnected
  while (!client.connected()) {
    // first check if connected to wifi
    if (WiFi.status() != WL_CONNECTED) {
      // if not connected, then first connect to wifi
      setup_wifi();
    }
    // now attemt to connect to MQTT server
    // Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_client")) {
      // attempt successful
      // Serial.println("connected");

      // Subscribe to topics here
      client.subscribe("esp32/data");
      client.subscribe("esp32/angle");
      client.subscribe("esp32/sms_state");
      client.subscribe("esp32/state");
      client.subscribe("esp32/CarSteer");
      client.publish("esp32/state", "1");
    } else {
      // attempt not successful
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" trying again in 2 seconds");
      delay(2000);
    }
  }
}

/*************************************************************
**************** Callback Func when data on ******************
********************* subscribed topics  *********************
**************************************************************/
void callback(char *topic, byte *message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Check if a message is received on the (sms_state) topic
  if (String(topic) == "esp32/sms_state") {
    if (messageTemp == "1") {
      Serial.println("=======================");
      Serial.println("Action: Driver Sleep");
      Serial.println("Action: Turn On buzzer");
      Serial.println("=======================");
      digitalWrite(Buzzer_pin, HIGH);
    }

    if (messageTemp == "0") {
      Serial.println("=======================");
      Serial.println("Action: Driver Awake");
      Serial.println("=======================");
      digitalWrite(Buzzer_pin, LOW);
    }
  }

  // Check if a message is received on the (CarSteer) topic
  if (String(topic) == "esp32/CarSteer") {
    // map from string to float then cast it to int
    float steer_angle_float = messageTemp.toFloat();
    float steer_angle_after_mapping = mapFloat(steer_angle_float, -1.0, 1.0, 180.0, -180.0);
    steer_angle_int = (int)steer_angle_after_mapping;

    // if current angle not equal prev angle (to avoid noise)
    // if (prev_steer_angle != steer_angle_int) {
      Serial.println("====================");
      Serial.println(steer_angle_int);
      // prev_steer_angle = steer_angle_int;
      Serial.println("====================");
    // }
  }
}


/*************************************************************
************************* Setup Func *************************
**************************************************************/
void setup() {
  pinMode(Buzzer_pin, OUTPUT);
  /*************************************************************
******************** Motor & encoder Setup *******************
**************************************************************/
  pinMode(R_IS, OUTPUT);
  pinMode(L_IS, OUTPUT);
  digitalWrite(L_IS, LOW);
  digitalWrite(R_IS, LOW);

  // config PWM channel with freq and resolution
  ledcSetup(PWM_channel0, freq, resolution);
  ledcSetup(PWM_channel1, freq, resolution);

  // attach the channel to the GPIO to be controlled
  ledcAttachPin(RPWM, PWM_channel0);
  ledcAttachPin(LPWM, PWM_channel1);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);

  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);


  Serial.begin(115200);
  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  encoder.attachHalfQuad(DT, CLK);
  encoder.setCount(0);
}

void loop() {
  if (!client.connected()) {
    connect_mqttServer();
  }
  client.loop();
  moveMotor(steer_angle_int);
  counter = encoder.getCount() / 2;
  Serial.println("speed");
  Serial.println(speed);
  Serial.println("counter");
  Serial.println(counter);
  Serial.println("direction");
  Serial.println(direction);

  // to publish data on topic use this example
  // client.publish("esp32/angle", "37");
}