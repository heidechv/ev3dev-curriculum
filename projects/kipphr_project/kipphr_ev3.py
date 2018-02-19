import mqtt_remote_method_calls as comm
import robot_controller as robo
import time
import ev3dev.ev3 as ev3


def main():
    robot = robo.Snatch3r()
    mqtt = comm.MqttClient(robot)
    mqtt.connect_to_pc()

    while robot.running:
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
            robot.turn_degrees(720, 500)
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
            robot.drive(900, 900)
            time.sleep(3.5)
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
            robot.stop()
            mqtt.send_message('stop_race')
            robot.running = False
        robot.drive(469, 469)