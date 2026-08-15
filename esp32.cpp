#include <Arduino.h>
#include <ESP32Servo.h>

float integral_x = 0;
float integral_y = 0;

float previous_error_x = 0;
float previous_error_y = 0;

unsigned long previoustime = 0;

const int x_pin = 18;
const int y_pin = 19;

Servo servo_x;
Servo servo_y;

float servo_x_position = 90;
float servo_y_position = 90;


int proportional(float error, float kp) 
{
    return error * kp;
}

int integral(float error, float ki, float dt,float integral)
{
    return integral += error * dt;
}

int derivative(float error, float kd, float dt, float previous_error)
{
    return kd*(error - previous_error) / dt;
}

int pid(float error, float kp, float ki, float kd, float dt,float integral, float previous_error)
{
    float proportional = proportional(error, kp);
    float integral = integral(error, ki, dt,integral);
    float derivative = derivative(error, kd, dt, previous_error);
    return proportional + integral + derivative;
}

void servomove(int position_x, int position_y)
{
    servo_x_position = constrain(position_x, 0, 180);
    servo_y_position = constrain(position_y, 0, 180);
    servo_x.write(servo_x_position);
    servo_y.write(servo_y_position);
}

void setup()
{
    Serial.begin(9600);
    previoustime = micros();

    servo_x.attach(x_pin);
    servo_y.attach(y_pin);
    
    servo_x.write(90);
    servo_y.write(90);

}

void loop()
{   
    ## X tuning values
    kpx = 0;
    kix =0;
    kdx = 0;

    ## Y tuning values
    kpy = 0;
    kiy = 0;
    kdy = 0;

    if (serial.available()> 0)
    {
        string input = serial.readStringUntil('\n');
        error_x = input.substring(0, input.indexOf(',')).toInt();
        error_y = input.substring(input.indexOf(',') + 1).toInt();

        unsigned long cutrrenttime = micros();
        float dt = (currenttime - previoustime) / 1000000f;
        previoustime = currenttime;



        move_x = pid(error_x, kpx, kix, kdx, dt, integral_x, previous_error_x);
        move_y = pid(error_y, kpy, kiy, kdy, dt, integral_y, previous_error_y);

        servo_move(servo_x_position + move_x, servo_y_position + move_y);
    }


}

