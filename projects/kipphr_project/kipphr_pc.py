import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self, root):
        self.root = root

    def shutdown(self):
        print('Exiting')
        self.root.destroy()
        exit()


def main():

    root = tkinter.Tk()
    root.title('Mario Kart!')

    my_del = MyDelegate(root)

    mqtt = com.MqttClient(my_del)
    mqtt.connect_to_ev3()

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=1, column=2)
    forward_button['command'] = lambda: move(mqtt, 'forward')
    root.bind('<Up>', lambda event: move(mqtt, 'forward'))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2, column=3)
    right_button['command'] = lambda: move(mqtt, 'right')
    root.bind('<Right>', lambda event: move(mqtt, 'right'))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2, column=1)
    left_button['command'] = lambda: move(mqtt, 'left')
    root.bind('<Left>', lambda event: move(mqtt, 'left'))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    left_button['command'] = lambda: move(mqtt, 'stop')
    root.bind('<space>', lambda event: move(mqtt, 'stop'))

    root.mainloop()


def move(mqtt, direction):
    mqtt.send_message('drive_by_colors', [direction])


main()
