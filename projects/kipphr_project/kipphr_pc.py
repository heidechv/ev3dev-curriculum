import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    mqtt = com.MqttClient()
    mqtt.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Go To A Color')

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=1, column=1)
    start_button['command'] = lambda: start_race(mqtt)
    root.bind('<space>', lambda: start_race(mqtt))

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=3, column=1)
    forward_button['command'] = lambda: forward(mqtt)
    root.bind('<Up>', lambda: forward(mqtt))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2, column=2)
    right_button['command'] = lambda: turn(mqtt, 'right')
    root.bind('<Right>', lambda: turn(mqtt, 'right'))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2, column=1)
    left_button['command'] = lambda: turn(mqtt, 'left')
    root.bind('<Left>', lambda: turn(mqtt, 'left'))

    root.mainloop()


def start_race(mqtt):
    mqtt.send_message('start_race')


def turn(mqtt, direction):
    if direction == 'right':
        mqtt.send_message('turn_right', [469])
    if direction == 'left':
        mqtt.send_message('turn_left', [469])


def forward(mqtt):
    mqtt.send_message('drive_by_colors')


main()
