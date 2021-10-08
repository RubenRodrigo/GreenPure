//Librerias
#include "DHT.h"
#include <TinyGPS++.h>           // Include TinyGPS++ library
#include <SoftwareSerial.h>      // Include software serial library
#include <Wire.h>
#include "RTClib.h"

#define Trigger   4
#define Echo      2

#define DHTPIN 3 //Sensor de temperatura y humedad
#define DHTTYPE DHT11 //Tipo de sensor de temperatura y humedad

#define MQ4Pin A0 // Sensor de metano
#define MQ2Pin A1 // Sensor gas combustible y humo

#define smallPM1 5 //Sensor de particulas
// Actuadores
#define led 6
#define led_rojo 8
#define led_GPS 13
#define buzzer 7

// --- Objetos ---
DHT dht(DHTPIN, DHTTYPE); // Humedad
TinyGPSPlus gps; // GPS
#define S_RX    12                // Define software serial RX pin
#define S_TX    11               // Define software serial TX pin
SoftwareSerial SoftSerial(S_RX, S_TX);    // Configure SoftSerial library
RTC_DS1307 rtc;
DateTime HoraFecha;

//Variables para el sensor de temperatura
float h, t, f, hif, hic;
  
//Variables para el detector de particulas
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 1000; 
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;

//Variables de sensor de gas
int gas_value_mq2;
int gas_value_mq4;
boolean mq2, mq4;

//Validación de la exportación de datos
boolean exportar;
byte  dato_serial;

//Variables de tiempo real
int segundo,minuto,hora,dia,mes;
long anio;

//Métodos de medición del aire
void TempHume(){
  //Medidor de temperatura
  h = dht.readHumidity();
  t = dht.readTemperature();
  f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  hif = dht.computeHeatIndex(f, h);
  hic = dht.computeHeatIndex(t, h, false);
  //Serial.print("H: "); Serial.print(h); Serial.print(" %\t"); Serial.print("T: ");  Serial.print(t); Serial.print(" *C "); Serial.print(f); Serial.println(" *F\t");
  //Serial.print("HI: "); Serial.print(hic); Serial.print(" *C "); Serial.print(hif); Serial.println(" *F");
}
void Parti(){
  ratio = lowpulseoccupancy/(sampletime_ms*10.0);  
  concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; 
  //Serial.print("Concentration = "); Serial.print(concentration);
  //Serial.println(" pcs/0.01cf");
  lowpulseoccupancy = 0;
  starttime = millis();
}
void Gas(){
  gas_value_mq2 = digitalRead(MQ2Pin);  
  gas_value_mq4 = digitalRead(MQ4Pin);

  if(gas_value_mq4==HIGH)
  { 
    //Serial.println("GAS MQ4 DETECTED"); 
    mq4 = true;
  }
  else
  {
    //Serial.println("GAS MQ4 NOT DETECTED");
    mq4 = false;
  }
  if(gas_value_mq2==HIGH){
    //Serial.println("GAS MQ2 DETECTED");
    mq2 = true;
  }else{
    //Serial.println("GAS MQ2 NOT DETECTED");
    mq2 = false;
  }
}

void Actuadores(int respuesta){
  if (respuesta == 1) {
    tone(buzzer, 1000);
    digitalWrite(led, HIGH);
    delay(500);
    noTone(buzzer);
    digitalWrite(led, LOW);
  }else {
    tone(buzzer, 1000);
    digitalWrite(led_rojo, HIGH);
    delay(500);
    noTone(buzzer);
    digitalWrite(led_rojo, LOW);
  }
}

void GPS(){
  while (SoftSerial.available() > 0) {
    if (gps.encode(SoftSerial.read())) {
      if (gps.location.isValid()) {
        //Serial.print("Latitude   = "); Serial.println(gps.location.lat(), 6);
        //Serial.print("Longitude  = "); Serial.println(gps.location.lng(), 6);
        digitalWrite(led_GPS,HIGH);
        exportar = true;
      }
    }
  }
}

void setup() {
  Serial.begin(9600);
  SoftSerial.begin(9600);
  
  pinMode(Trigger, OUTPUT);  
  pinMode(Echo, INPUT);     
  digitalWrite(Trigger, LOW);
  dht.begin();
  
  pinMode(MQ4Pin, INPUT_PULLUP);
  pinMode(MQ2Pin, INPUT_PULLUP);

  pinMode(led, OUTPUT);
  pinMode(led_rojo, OUTPUT);
  pinMode(led_GPS, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  pinMode (smallPM1, INPUT);
  starttime = millis();

  rtc.begin();
}

void loop(){
  HoraFecha = rtc.now(); //obtenemos la hora y fecha actual
  //Medir datos
  TempHume(); 
  Gas();
  GPS();
  
  duration = pulseIn(smallPM1, LOW);
  lowpulseoccupancy = lowpulseoccupancy+duration;
  if ((millis()-starttime) >= sampletime_ms) //if the sampel time = = 5s
  {
    Parti();
    if(exportar){
      //Datos de la temperatura
      Serial.print(h); Serial.print(","); Serial.print(t); Serial.print(",");
      Serial.print(hic); Serial.print(",");
      //Datos de los sensores de gas
      Serial.print(mq4); Serial.print(","); Serial.print(mq2); Serial.print(",");
      //Datos del GPS
      Serial.print(gps.location.lat(), 6); Serial.print(","); Serial.print(gps.location.lng(), 6); Serial.print(",");
      Serial.print(HoraFecha.year()); Serial.print("-"); Serial.print(HoraFecha.month()); Serial.print("-"); Serial.print(HoraFecha.day()); Serial.print("T"); Serial.print(HoraFecha.hour()); Serial.print(":"); Serial.print(HoraFecha.minute()); Serial.print(":"); Serial.print(HoraFecha.second()); Serial.print("Z"); Serial.print(",");
      //Dato de las particulas
      Serial.println(concentration);
    }
  }
  
  //Actuadores();
  if (Serial.available()){
    dato_serial=Serial.read();
    if (dato_serial == '1'){
      Actuadores(1);
    }else if (dato_serial == '2') {
      Actuadores(2);
    }
  }
}
