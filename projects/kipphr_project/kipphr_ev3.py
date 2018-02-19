import mqtt_remote_method_calls as comm
import robot_controller as robo
import time


def main():
    robot = robo.Snatch3r()
    mqtt = comm.MqttClient(robot)
    mqtt.connect_to_pc()

    while not robot.touch_sensor.is_pressed:
        while robot.race:
            time.sleep(.1)

        mqtt.send_message('stop_race')

    mqtt.close()
    robot.shutdown()


main()
