// ============================================================
//  nano_left.ino — Baguette GAUCHE (Arduino Nano + MPU6050)
//
//  Protocole : "L,ax,ay,az,gx,gy,gz" @ 200 Hz, 115200 bauds
//    - accel : ±2 g  -> 16384 LSB/g
//    - gyro  : ±250 °/s -> 131 LSB/(°/s)
//    - valeurs brutes int (pas de float, pas de timestamp : le PC horodate)
//    - bannière "L" au boot pour l'identification automatique du port
//
//  Bibliothèques requises (gestionnaire de bibliothèques Arduino) :
//    - "Adafruit MPU6050"  (dépend d'"Adafruit Unified Sensor")
//  Câblage I2C : SDA->A4, SCL->A5, VCC->5V, GND->GND
// ============================================================
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

#define STICK_SIDE  'L'        // préfixe de chaque trame
#define STICK_NAME  "L"        // bannière d'identification
#define SAMPLE_HZ   200
#define LED_PIN     LED_BUILTIN

Adafruit_MPU6050 mpu;
static const uint32_t PERIOD_US = 1000000UL / SAMPLE_HZ;
static uint32_t nextTick = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  delay(300);                       // laisse l'USB s'énumérer

  Wire.begin();
  Wire.setClock(400000L);           // I2C à 400 kHz

  if (!mpu.begin(0x68)) {
    Serial.println("ERR MPU6050 NOT FOUND - halting");
    while (true) {                  // LED clignotante = erreur d'init
      digitalWrite(LED_PIN, !digitalRead(LED_PIN));
      delay(100);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);   // filtre passe-bas interne

  Serial.print("HELLO ");
  Serial.println(STICK_NAME);
  Serial.flush();
  nextTick = micros();
  digitalWrite(LED_PIN, HIGH);      // LED fixe = OK
}

void loop() {
  int32_t now = (int32_t)micros();
  if ((int32_t)(now - (int32_t)nextTick) < 0) return;   // pas encore l'heure

  // interruption longue (bug) : on resynchronise au lieu d'empiler du retard
  if ((uint32_t)(now - nextTick) > 10UL * PERIOD_US) {
    nextTick = (uint32_t)now;
  }
sensors_event_t a, g, temp;
mpu.getEvent(&a, &g, &temp);

Serial.print((char)STICK_SIDE);
Serial.print(',');

Serial.print((int)(a.acceleration.x * 1000));
Serial.print(',');

Serial.print((int)(a.acceleration.y * 1000));
Serial.print(',');

Serial.print((int)(a.acceleration.z * 1000));
Serial.print(',');

Serial.print((int)(g.gyro.x * 1000));
Serial.print(',');

Serial.print((int)(g.gyro.y * 1000));
Serial.print(',');

Serial.println((int)(g.gyro.z * 1000));

  nextTick += PERIOD_US;
}
