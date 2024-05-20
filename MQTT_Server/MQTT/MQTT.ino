#include <WiFi.h>
#include <PubSubClient.h>

/*************************************************************
******************** Define Network Config *******************
*************************************************************/
const char *ssid = "WE_D28CA0";
const char *password = "31097022";
const char *mqtt_server = "192.168.1.138"; // RPI ip

volatile int counter = 0; // encoder counter
const int pulses_per_revolution = 360;
int prev_steer_angle = 0;

/*************************************************************
************************* define pins ************************
*************************************************************/
#define Buzzer_pin 2
#define R_EN = 25;
#define L_EN = 26;
#define R_PWM = 32;
#define L_PWM = 33;
#define low1 34
#define low2 35
#define intruppt0 12
#define intruppt1 13
/*************************************************************
******************* define const variables *******************
************************** for PWM ***************************
*************************************************************/
const int freq = 5000;
const int PWM_channel0 = 0;
const int PWM_channel1 = 1;
const int resolution = 8;

WiFiClient espClient;
PubSubClient client(espClient);

/*************************************************************
********** Function to move motor to specific angle **********
*************************************************************/
void moveMotor(int angle)
{
    int error = angle - counter;
    while (error)
    {
        error = angle - counter;
        if (error > 5)
        {
            ledcWrite(PWM_channel1, 0);
            ledcWrite(PWM_channel0, 80); // change PWM to control motors speed
        }
        else if (error < -5)
        {
            ledcWrite(PWM_channel1, 80);
            ledcWrite(PWM_channel0, 0);
        }
        else
        {
            error = 0;
            ledcWrite(PWM_channel0, 0);
            ledcWrite(PWM_channel1, 0);
        }
    }
}

/*************************************************************
************************ interuppt ISR ***********************
**************************************************************/
void ai0()
{
    if (digitalRead(intruppt0) == LOW) // falling edge
    {                                  // CCW
        counter--;
    }
    else // CW
    {
        counter++;
    }
}

/*************************************************************
********************** Map Float value Func ******************
**************************************************************/
float mapFloat(float value, float in_min, float in_max, float out_min, float out_max)
{
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

/*************************************************************
************************* Wifi Setup *************************
**************************************************************/
void setup_wifi()
{
    delay(50);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000); //
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
void connect_mqttServer()
{
    // Loop until we're reconnected
    while (!client.connected())
    {
        // first check if connected to wifi
        if (WiFi.status() != WL_CONNECTED)
        {
            // if not connected, then first connect to wifi
            setup_wifi();
        }
        // now attemt to connect to MQTT server
        // Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("ESP32_client"))
        {
            // attempt successful
            // Serial.println("connected");

            // Subscribe to topics here
            client.subscribe("esp32/data");
            client.subscribe("esp32/angle");
            client.subscribe("esp32/sms_state");
            client.subscribe("esp32/state");
            client.subscribe("esp32/CarSteer");
            client.publish("esp32/state", "1");
        }
        else
        {
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
void callback(char *topic, byte *message, unsigned int length)
{
    Serial.print("Message arrived on topic: ");
    Serial.print(topic);
    Serial.print(". Message: ");
    String messageTemp;

    for (int i = 0; i < length; i++)
    {
        Serial.print((char)message[i]);
        messageTemp += (char)message[i];
    }
    Serial.println();

    // Check if a message is received on the (sms_state) topic 
    if (String(topic) == "esp32/sms_state")
    {
        if (messageTemp == "1")
        {
            Serial.println("=======================");
            Serial.println("Action: Driver Sleep");
            Serial.println("Action: Turn On buzzer");
            Serial.println("=======================");
            digitalWrite(Buzzer_pin, HIGH);
        }

        if (messageTemp == "0")
        {
            Serial.println("=======================");
            Serial.println("Action: Driver Awake");
            Serial.println("=======================");
            digitalWrite(Buzzer_pin, LOW);
        }
    }

    // Check if a message is received on the (CarSteer) topic 
    if (String(topic) == "esp32/CarSteer")
    {
        // map from string to float then cast it to int
        float steer_angle_float = messageTemp.toFloat();
        float steer_angle_after_mapping = mapFloat(steer_angle_float, -1.0, 1.0, -180.0, 180.0);
        int steer_angle_int = (int)steer_angle_after_mapping;

        // if current angle not equal prev angle (to avoid noise)
        if (prev_steer_angle != steer_angle_int) 
        {
            Serial.println("====================");
            Serial.println(steer_angle_int);
            prev_steer_angle = steer_angle_int;
            moveMotor(steer_angle_int);
            Serial.println("====================");
        }
    }
}


/*************************************************************
************************* Setup Func *************************
**************************************************************/
void setup()
{
    pinMode(Buzzer_pin, OUTPUT);
    pinMode(low1, OUTPUT);
    pinMode(low2, OUTPUT);
    digitalWrite(low1, LOW);
    digitalWrite(low2, LOW);

    // config PWM channel with freq and resolution 
    ledcSetup(PWM_channel0, freq, resolution);
    ledcSetup(PWM_channel1, freq, resolution);

    // attach the channel to the GPIO to be controlled
    ledcAttachPin(R_PWM, PWM_channel0);
    ledcAttachPin(L_PWM, PWM_channel1);

    pinMode(R_EN, OUTPUT); 
    pinMode(L_EN, OUTPUT);  

    digitalWrite(R_EN, HIGH); 
    digitalWrite(L_EN, HIGH); 

    pinMode(intruppt0, INPUT_PULLUP); 
    pinMode(intruppt1, INPUT_PULLUP); 

    attachInterrupt(intruppt1, ai0, FALLING); // define intruppt1 to take action on FALLING edge

    Serial.begin(115200);
    setup_wifi();

    client.setServer(mqtt_server, 1883); 
    client.setCallback(callback);
}

void loop()
{
    if (!client.connected())
    {
        connect_mqttServer();
    }
    client.loop();

    // to publish data on topic use this example
    // client.publish("esp32/angle", "37");
}