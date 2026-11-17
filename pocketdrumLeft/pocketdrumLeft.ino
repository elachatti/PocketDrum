#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Raw sensor values
int16_t ax, ay, az;
int16_t gx, gy, gz;

void setup()
{
    Serial.begin(115200);

    Wire.begin();

    mpu.initialize();

    if (!mpu.testConnection())
    {
        Serial.println("ERROR");
        while (1);
    }

    Serial.begin(9600);
    Wire.begin();
    mpu.initialize();

    Serial.print("Device ID: 0x");
    Serial.println(mpu.getDeviceID(), HEX);

    if (!mpu.testConnection())
    {
        Serial.println("testConnection failed, continuing anyway");
    }
}

void loop()
{
    mpu.getMotion6(
        &ax,
        &ay,
        &az,
        &gx,
        &gy,
        &gz
    );

    Serial.print("L,");
    Serial.print(ax);
    Serial.print(",");
    Serial.print(ay);
    Serial.print(",");
    Serial.print(az);
    Serial.print(",");
    Serial.print(gx);
    Serial.print(",");
    Serial.print(gy);
    Serial.print(",");
    Serial.println(gz);

    delay(5);   // about 200 Hz
}
