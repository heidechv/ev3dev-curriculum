#'Satya Arcot'
#"EV3 Final Project CSSE120"
#'CSSE120 Session 2 Dr. Fisher'


import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com


class Delegate(object):
    def __init__(self, robot):
        self.robot = robot

    def chase_the_ball(self):
        print('Chase the ball')
        ev3.Sound.speak('Time for some cardio').wait()
        while True:
            front_sensor = self.robot.ir_sensor.proximity
            print(front_sensor)
            if front_sensor < 45:
                self.robot.drive(300, 300)
            elif front_sensor > 30:
                self.robot.stop()
                ev3.Sound.speak('I am tired')

    def spin_for_the_ball(self):
        ev3.Sound.speak('Time to work my obliques').wait()
        while True:
            pixy_x = self.robot.find_color
            print(pixy_x)
            if pixy_x is None:
                self.robot.drive(30, -30)
            elif pixy_x < 140:
                self.robot.drive(-30, 30)
            elif pixy_x > 170:
                self.robot.drive(30, -30)
            else:
                self.robot.stop()
                ev3.Sound.speak('I am tired')


""" The robot will display through an mqtt client  """


def main():
    print('--------------------')
    print('Chasing the carrot')
    print('--------------------')
    robot = robo.Snatch3r()
    delegate = Delegate(robot)
    mqtt_client = com.MqttClient(delegate)
    mqtt_client.connect_to_pc()
    ev3.Sound.speak('I want the carrot').wait()
    robot.loop_forever()


main()
