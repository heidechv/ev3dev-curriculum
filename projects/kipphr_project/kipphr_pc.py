import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class DataContainer(object):
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def stop_race(self):
        self.end_time = time.time()


def main():
    robot = robo.Snatch3r()
    dc = DataContainer()

    mqtt = com.MqttClient(dc)
    mqtt.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Go To A Color')

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=1, column=1)
    start_button['command'] = lambda: start_race(mqtt, dc)
    root.bind('<space>', lambda: start_race(mqtt, dc))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2, column=2)
    right_button['command'] = lambda: turn(mqtt, 'right')
    root.bind('<right>', lambda: turn(mqtt, 'right'))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2, column=1)
    left_button['command'] = lambda: turn(mqtt, 'left')
    root.bind('<left>', lambda: turn(mqtt, 'left'))

    time_label = ttk.Label(main_frame, text='Time: ')
    time_label.grid(row=1, column=2)

    race_time = ttk.Label(main_frame, text=(dc.end_time - dc.start_time))
    race_time.grid(row=1, column=3)

    root.mainloop()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


def start_race(mqtt, dc):
    dc.start_time = time.time()
    mqtt.send_message('start_race')


def turn(mqtt, direction):
    if direction == 'right':
        mqtt.send_message('turn_right', [469])
    if direction == 'left':
        mqtt.send_message('turn_left', [469])


main()
