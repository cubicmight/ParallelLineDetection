import time
from adafruit_servokit import ServoKit

# Initialize the PCA9685 board
pca = ServoKit(channels=16)

# Set the PWM frequency (50 Hz is recommended for servos)
pca.frequency = 50

# Set the minimum and maximum pulse lengths for your servos
SERVO_MIN = 150  # Minimum pulse length out of 4096
SERVO_MAX = 600  # Maximum pulse length out of 4096

# Define the servo channels for your robot
LEFT_WHEEL_CHANNEL = 0
RIGHT_WHEEL_CHANNEL = 1

# Define the speed and direction of your robot
SPEED = 0.5
LEFT = -1
RIGHT = 1

def stop_robot():
    pca.servo[LEFT_WHEEL_CHANNEL].angle = 90
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = 90

def move_forward():
    pca.servo[LEFT_WHEEL_CHANNEL].angle = SERVO_MIN
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = SERVO_MAX

def move_backward():
    pca.servo[LEFT_WHEEL_CHANNEL].angle = SERVO_MAX
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = SERVO_MIN

def turn_left():
    pca.servo[LEFT_WHEEL_CHANNEL].angle = SERVO_MAX
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = SERVO_MAX

def turn_right():
    pca.servo[LEFT_WHEEL_CHANNEL].angle = SERVO_MIN
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = SERVO_MIN

def move(speed, direction):
    left_speed = SPEED * speed * direction
    right_speed = SPEED * speed * direction
    pca.servo[LEFT_WHEEL_CHANNEL].angle = int(90 + left_speed * (SERVO_MAX - SERVO_MIN))
    pca.servo[RIGHT_WHEEL_CHANNEL].angle = int(90 + right_speed * (SERVO_MAX - SERVO_MIN))

try:
    while True:
        # Read the user input
        cmd = input("Enter a command (f = forward, b = backward, l = left, r = right, s = stop): ")

        # Move the robot based on the user input
        if cmd == 'f':
            move_forward()
        elif cmd == 'b':
            move_backward()
        elif cmd == 'l':
            turn_left()
        elif cmd == 'r':
            turn_right()
        elif cmd == 's':
            stop_robot()
        else:
            print("Invalid command")

except KeyboardInterrupt:
    # Stop the robot and clean up
    stop_robot()
