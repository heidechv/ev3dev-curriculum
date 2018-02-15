'Satya Arcot'
"EV3 Final Project CSSE120"
'CSSE120 Session 2 Dr. Fisher'

import ev3dev.ev3 as ev3
import time
import robot_controller as robo



class My_delegate(object):
    def __init__(self):
        self.running = True


    def spin_for_the_ball(robot):
        ev3.Sound.speak('Time to work my obliques').wait()
        while True:
            pixy_x = robot.get_pixy_x()
            print(pixy_x)
            if pixy_x is None:
                robot.start_moving(30, -30)
            elif pixy_x < 140:
                robot.start_moving(-30, 30)
            elif pixy_x > 170:
                robot.start_moving(30, -30)
            else:
                robot.stop_moving()
                ev3.Sound.speak('I am tired')

    def chase_the_ball(robot):
        ev3.Sound.speak('Time for some cardio').wait()
        while True:
            front_sensor = robot.get_front_proximity_sensor_reading()
            print(front_sensor)
            if front_sensor < 420:
                robot.start_moving(40, 40)
            elif front_sensor > 550:
                robot.stop_moving()
            else:
                robot.stop_moving()
                ev3.Sound.speak('I am tired')


""" The robot will display through an mqtt client  """

def main():
    print('--------------------')
    print('Chasing the carrot')
    print('--------------------')
    ev3.Sound.speak('I want the carrot').wait()
