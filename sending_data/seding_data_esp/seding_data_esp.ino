#include <WiFi.h>
#include <HTTPClient.h>

WiFiServer server(80);

#define led 2
const char *ssid = "EC";
const char *password = "Hunter1235";
int angle =0 ;
int gps = 0 ;

IPAddress local_ip(192, 168, 1, 4);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

void setup()
{
    Serial.begin(115200);
    Serial.println("Ready.");
    WiFi.softAP(ssid, password);
    WiFi.softAPConfig(local_ip, gateway, subnet);
    Serial.println("");
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    IPAddress IP = WiFi.softAPIP();
    Serial.println(IP);
    server.begin();
    pinMode(led, OUTPUT);
}

void loop()
{
    WiFiClient client = server.available();
    if (!client)
    {
        return;
    }
    while (!client.available())
    {
        delay(1);
    }

    String request = client.readStringUntil('\r');
    // Serial.println(request);
    client.flush();

    int angleIndex = request.indexOf("angle=");
    int GpsIndex = request.indexOf("gps=");

    if (angleIndex != -1)
    {
        angle = request.substring(angleIndex + 6).toInt();
        Serial.println("===================");
        Serial.print("Received angle: ");
        Serial.println(angle);
        analogWrite(led, angle);
    }
    if (GpsIndex != -1)
    {
        gps = request.substring(GpsIndex + 4).toInt();
        Serial.print("Received gps: ");
        Serial.println(gps);
        Serial.println("===================");
    }
    
    // Send HTTP response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.print("angle : ");
    client.println(angle);
    client.print("gps : ");
    client.println(gps);
}
