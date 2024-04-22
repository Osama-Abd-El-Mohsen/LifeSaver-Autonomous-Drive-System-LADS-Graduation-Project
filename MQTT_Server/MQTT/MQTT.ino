#include <WiFi.h>
#include <PubSubClient.h>

#define ledPin 2

long lastMsg = 0;
const char *ssid = "Error404";
const char *password = "Unti1W3M33tAgainbuddy";
const char *mqtt_server = "192.168.1.5";

WiFiClient espClient;
PubSubClient client(espClient);

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
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("ESP32_client"))
        {
            // attempt successful
            Serial.println("connected");

            // Subscribe to topics here
            client.subscribe("esp32/data");
            client.subscribe("esp32/angle");
            client.subscribe("esp32/sms_state");
            client.subscribe("esp32/state");
            client.publish("esp32/state", "Esp connected");
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

// this function will be executed whenever there is data available on subscribed topics
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

    // Check if a message is received on the topic 
    if (String(topic) == "esp32/sms_state")
    {
        if (messageTemp == "1")
        {
            Serial.println("=======================");
            Serial.println("Action: Driver Sleep");
            Serial.println("Action: Turn On buzzer");
            Serial.println("=======================");
            digitalWrite(ledPin,HIGH);
        }

        if (messageTemp == "0")
        {
            Serial.println("=======================");
            Serial.println("Action: Driver Awake");
            Serial.println("=======================");
            digitalWrite(ledPin,LOW);
        }
    }
}

void setup()
{
    pinMode(ledPin, OUTPUT);
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
    long now = millis();
    // if (now - lastMsg > 4000) {
    //   lastMsg = now;
    //   //topic name (to which this ESP32 publishes its data). 37 is the dummy value.
    //   client.publish("esp32/angle", "37");
    // }
}