from machine import PWM, ADC, Pin
import math
import utime

# Joystick connections
adc_x_joystick = ADC(Pin(26))
adc_y_joystick = ADC(Pin(27))
sw_joystick = Pin(16, Pin.IN, Pin.PULL_UP)
servo_x = PWM(Pin(0), freq=50)
servo_y = PWM(Pin(1), freq=50)
servo_switch = PWM(Pin(2), freq=50)  # Define PWM for the switch servo

def get_joystick_value(joystick_position, joystick_min, joystick_max, desired_min, desired_max):
    m = ((desired_min - desired_max) / (joystick_min - joystick_max))
    return int((m * joystick_position) - (m * joystick_max) + desired_max)

def get_servo_duty_cycle(joystick_value, min_angle_ms, max_angle_ms, period_ms, desired_min, desired_max):
    point_1_x = desired_min
    point_1_y = (min_angle_ms / period_ms) * 65536
    point_2_x = desired_max
    point_2_y = (max_angle_ms / period_ms) * 65535
    m = (point_2_y - point_1_y) / (point_2_x - point_1_x)
    return int((m * joystick_value) - (m * desired_min) + point_1_y)

def get_y_joystick_value(joystick_position, joystick_min, joystick_max, desired_min, desired_max):
    m = ((desired_min - desired_max) / (joystick_min - joystick_max))
    return int((m * joystick_position) - (m * joystick_max) + desired_max)

def get_y_servo_duty_cycle(joystick_value, min_angle_ms, max_angle_ms, period_ms, desired_min, desired_max):
    point_1_x = desired_min
    point_1_y = (min_angle_ms / period_ms) * 65536
    point_2_x = desired_max
    point_2_y = (max_angle_ms / period_ms) * 65535
    m = (point_2_y - point_1_y) / (point_2_x - point_1_x)
    return int((m * joystick_value) - (m * desired_min) + point_1_y)

while True:
    x_position = adc_x_joystick.read_u16() 
    y_position = adc_y_joystick.read_u16()
    sw_status = sw_joystick.value()        
    
    x_value = get_joystick_value(x_position, 416, 65535, -100, 100)
    y_value = get_y_joystick_value(y_position, 416, 65535, -100, 100)
    
    range_of_values = math.sqrt(x_value ** 2)
    if range_of_values <= 8:
        x_value = 0
        
    range_of_values = math.sqrt(y_value ** 2)
    if range_of_values <= 8:
        y_value = 0
        
    x_duty = get_servo_duty_cycle(x_value, 0.5, 2.5, 20, -100, 100)
    y_duty = get_y_servo_duty_cycle(y_value, 0.5, 2.5, 20, -100, 100)
    
    if sw_status == 0:
        sw_duty = int((2.5 * 65535) / 20)
    else:
        sw_duty = int((0.5 * 65535) / 20)
    
    servo_x.duty_u16(x_duty)
    servo_y.duty_u16(y_duty)
    servo_switch.duty_u16(sw_duty)
    
    print(f"x_value is: {x_value}, x_duty is: {x_duty}, y_value is: {y_value}, y_duty is: {y_duty}, sw_status is: {sw_status}, sw_duty is: {sw_duty}")
    
    utime.sleep(0.1)

