'Satya Arcot'
"EV3 Final Project CSSE120"
'CSSE120 Session 2 Dr. Fisher'

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com

class Delegate(object):
    def __init__(self, robot):
        self.robot = robot
    def chase_the_ball(self):
        print('Chase the ball')
        ev3.Sound.speak('Time for some cardio').wait()
        while True:
            front_sensor = self.robot.get_front_proximity_sensor_reading()
            print(front_sensor)
            if front_sensor < 420:
                self.robot.start_moving(40, 40)
            elif front_sensor > 550:
                self.robot.stop_moving()
            else:
                self.robot.stop_moving()
                ev3.Sound.speak('I am tired')


robot = robo.Snatch3r()
delegate = Delegate(robot)
mqtt_client = com.MqttClient(delegate)
mqtt_client.connect_to_pc()



def spin_for_the_ball(self, robo):
    ev3.Sound.speak('Time to work my obliques').wait()
    while True:
        pixy_x = robo.get_pixy_x()
        print(pixy_x)
        if pixy_x is None:
            robot.drive(30, -30)
        elif pixy_x < 140:
            robot.drive(-30, 30)
        elif pixy_x > 170:
            robot.drive(30, -30)
        else:
            robot.stop()
            ev3.Sound.speak('I am tired')


""" The robot will display through an mqtt client  """

def main():
    print('--------------------')
    print('Chasing the carrot')
    print('--------------------')
    ev3.Sound.speak('I want the carrot').wait()
    robot.loop_forever()


main()
