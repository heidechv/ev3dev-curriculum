import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo

class DataContainer(object):
    def __init__(self):



class MyDelegate(object):
    def shutdown(self):
        print('Exiting')
        exit()


def main():
    robot = robo.Snatch3r()
    dc = DataContainer()

    my_delegate = MyDelegate()

    mqtt = com.MqttClient(my_delegate)
    mqtt.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Go To A Color')

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    red_button = ttk.Button(main_frame, text="Go To Red")
    red_button.grid(row=1, column=1)
    red_button['command'] = lambda: drive_to_color(ev3.ColorSensor.COLOR_RED)

    white_button = ttk.Button(main_frame, text="Go To White")
    white_button.grid(row=1, column=2)
    white_button['command'] = lambda: drive_to_color(ev3.ColorSensor.COLOR_WHITE)

    black_button = ttk.Button(main_frame, text="Go To Black")
    black_button.grid(row=1, column=3)
    black_button['command'] = lambda: drive_to_color(ev3.ColorSensor.COLOR_BLACK)

    root.mainloop()


def drive_to_color(color_to_seek):
    ev3.Sound.speak("Seeking your color").wait()

    robot.drive(600, 600)

    while True:
        if robot.color_sensor.color == color_to_seek:
            robot.stop()
            break

    ev3.Sound.speak("Found your color").wait()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


def enter_pressed(dc, mqtt):
    for k in range(len(dc.color_order)):
        mqtt.send_message('find_color', [dc.color_sig[k], dc.color_order[k]])
        print(dc.color_order[k], dc.color_sig[k])
    dc.color_order = []
    dc.color_sig = []


main()
