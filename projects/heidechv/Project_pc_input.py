import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class DataContainer(object):

    def __init__(self):
        self.color_order = []
        self.color_sig = []


class MyDelegate(object):

    def __init__(self, root):
        self.root = root

    def shutdown(self):
        print('Exiting')
        self.root.destroy()
        exit()


def main():
    root = tkinter.Tk()
    root.title('Simon Says')

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    blue_button = tkinter.Button(main_frame, bg="Blue", height=1, width=9)
    blue_button.grid(row=1, column=2)
    blue_button['command'] = lambda: blue_pressed(dc)

    green_button = tkinter.Button(main_frame, bg="Green", height=1, width=9)
    green_button.grid(row=2, column=1)
    green_button['command'] = lambda: green_pressed(dc)

    red_button = tkinter.Button(main_frame, bg="Red", height=1, width=9)
    red_button.grid(row=2, column=3)
    red_button['command'] = lambda: red_pressed(dc)

    yellow_button = tkinter.Button(main_frame, bg="Yellow", height=1, width=9)
    yellow_button.grid(row=3, column=2)
    yellow_button['command'] = lambda: yellow_pressed(dc)

    enter_button = ttk.Button(main_frame, text='Enter')
    enter_button.grid(row=2, column=2)
    enter_button['command'] = lambda: enter_pressed(dc, mqtt)

    dc = DataContainer()

    my_delegate = MyDelegate(root)

    mqtt = com.MqttClient(my_delegate)
    mqtt.connect_to_ev3()

    root.mainloop()


def blue_pressed(dc):
    dc.color_order = dc.color_order + ['Blue']
    dc.color_sig = dc.color_sig + ['SIG1']
    print(dc.color_order)


def green_pressed(dc):
    dc.color_order = dc.color_order + ['Green']
    dc.color_sig = dc.color_sig + ['SIG2']
    print(dc.color_order)


def red_pressed(dc):
    dc.color_order = dc.color_order + ['Red']
    dc.color_sig = dc.color_sig + ['SIG3']
    print(dc.color_order)


def yellow_pressed(dc):
    dc.color_order = dc.color_order + ['Yellow']
    dc.color_sig = dc.color_sig + ['SIG4']
    print(dc.color_order)


def enter_pressed(dc, mqtt):
    for k in range(len(dc.color_order)):
        mqtt.send_message('find_color', [dc.color_sig[k], dc.color_order[k]])
        print(dc.color_order[k], dc.color_sig[k])
    dc.color_order = []
    dc.color_sig = []


main()
