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

    def drive_inches(self, inches_target, speed_deg_per_second):
        "Robot drives for the inputted distance at the inputted speed"
        degrees = inches_target * 90
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=degrees, stop_action='brake')
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=degrees, stop_action='brake')

    def turn_degrees(self, degrees_to_turn, speed_deg_per_second):
        "Robot turns the inputted degrees at the inputted speed"
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

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

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

    def drive(self,left_speed, right_speed):
        self.left_motor.run_forever(speed=left_speed)
        self.right_motor.run_forever(speed=right_speed)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

