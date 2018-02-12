import mqtt_remote_method_calls as com
import robot_controller as robo
import time


def main():
    robot = robo.Snatch3r()

    mqtt = com.MqttClient(robot)
    mqtt.connect_to_pc()

    while not robot.touch_sensor.is_pressed:
        time.sleep(.1)

    mqtt.send_message("shutdown")
    robot.shutdown()
    mqtt.connect_to_pc()


main()
