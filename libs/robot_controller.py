"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert self.left_motor
        assert self.right_motor

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        assert self.arm_motor
        assert self.touch_sensor

        self.running = None

        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy

    def drive_inches(self, inches_target, speed_deg_per_second):
        """"Robot drives for the inputted distance at the inputted speed"""
        degrees = inches_target * 90
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=degrees, stop_action='brake')
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=degrees, stop_action='brake')

    def turn_degrees(self, degrees_to_turn, speed_deg_per_second):
        """"Robot turns the inputted degrees at the inputted speed"""
        degrees_to_turn = degrees_to_turn * (450/90)
        if degrees_to_turn < 0:
            self.right_motor.run_to_rel_pos(speed_sp=-speed_deg_per_second, position_sp=degrees_to_turn)
            self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=-degrees_to_turn)
        else:
            self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=degrees_to_turn)
            self.left_motor.run_to_rel_pos(speed_sp=-speed_deg_per_second, position_sp=-degrees_to_turn)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """Calibrates the arm by raising it up and all the way down. Then sets that position to zero."""
        self.arm_motor.run_forever(speed_sp=800)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        """Raises the robot's arm all the way up"""
        self.arm_motor.run_forever(speed_sp=800)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

    def arm_down(self):
        """Lowers the robot's arm all the way down"""
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

    def loop_forever(self):
        """Creates an Infinite loop"""
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        """ Ends the Infinite loop"""
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak("Goodbye").wait()

    def drive(self, left_speed, right_speed):
        """Drives robot at inputted motor speeds"""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):
        """Stops robot"""
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def turn_right(self, motor_speed):
        """Robot turns right at given speed"""
        self.left_motor.run_forever(speed_sp=motor_speed)
        self.right_motor.run_forever(speed_sp=-motor_speed)

    def turn_left(self, motor_speed):
        """Robot turns left at given speed"""
        self.left_motor.run_forever(speed_sp=-motor_speed)
        self.right_motor.run_forever(speed_sp=motor_speed)

    def seek_beacon(self):
        """Robot finds and picks up the beacon"""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 200
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance

            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.turn_left(100)

            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 1:
                        self.drive(forward_speed, forward_speed)
                    else:
                        self.drive_inches(2.75, 200)
                        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
                        self.stop()
                        return True
                if 2 < math.fabs(current_heading) < 10:
                    print("Adjust heading: ", current_heading)
                    if current_heading < 0:
                        self.turn_left(turn_speed)
                    if current_heading > 0:
                        self.turn_right(turn_speed)

                if math.fabs(current_heading) > 10:
                    self.turn_left(100)
                    print("Heading too far off:", current_heading)

            time.sleep(0.2)

        print("Abandon ship!")
        self.stop()
        return False

    def find_color(self, color_sig, color):
        self.pixy.mode = color_sig
        turn_speed = 100

        color_found = False

        while not color_found:
            x = self.pixy.value(1)

            if x < 150:
                self.turn_left(turn_speed)
            elif x > 170:
                self.turn_right(turn_speed)
            elif 150 < x < 170:
                self.stop()
                color_found = True

            time.sleep(0.25)

        ev3.Sound.speak(color).wait()

    def dance(self, speed):
        self.drive(speed, speed)
        while True:
            if self.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                self.stop()
                self.arm_up()
                self.arm_down()
                self.drive(speed, speed)
            if self.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                self.stop()
                self.drive(speed, -speed)
                self.stop()
                self.drive(speed, speed)

    def drive_by_colors(self, direction):
        if direction == 'right':
            self.turn_right(150)
        if direction == 'left':
            self.turn_left(150)
        if direction == 'stop':
            self.stop()
        if direction == 'forward':
            self.drive(150, 150)
            if self.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                self.turn_degrees(720, 500)
                self.drive(150, 150)
            if self.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                self.drive(900, 900)
                time.sleep(3)
                self.drive(150, 150)