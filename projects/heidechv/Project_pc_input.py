import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time


class DataContainer(object):

    def __init__(self):
        self.color_order = []


class MyDelegate(object):
    def __init__(self):
        self.state = True

    def shutdown(self):
        self.state = False



def main():
    dc = DataContainer()

    my_delegate = MyDelegate()

    mqtt = com.MqttClient(my_delegate)
    mqtt.connect_to_ev3()

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    blue_button = ttk.Button(main_frame, text="Blue")
    blue_button.grid(row=1, column=2)
    blue_button['command'] = lambda: blue_pressed(dc)

    green_button = ttk.Button(main_frame, text="Green")
    green_button.grid(row=2, column=1)
    green_button['command'] = lambda: green_pressed(dc)

    red_button = ttk.Button(main_frame, text="Red")
    red_button.grid(row=2, column=3)
    red_button['command'] = lambda: red_pressed(dc)

    yellow_button = ttk.Button(main_frame, text="Yellow")
    yellow_button.grid(row=3, column=2)
    yellow_button['command'] = lambda: yellow_pressed(dc)

    enter_button = ttk.Button(main_frame, text='Enter')
    enter_button.grid(row=2, column=2)
    enter_button['command'] = lambda: enter_pressed(dc)

    root.mainloop()

    while my_delegate.state:
        time.sleep(.1)

    print('Exiting')
    mqtt.close()
    exit()

def blue_pressed(dc):
    dc.color_order = dc.color_order + ['blue']
    print(dc.color_order)


def green_pressed(dc):
    dc.color_order = dc.color_order + ['green']
    print(dc.color_order)


def red_pressed(dc):
    dc.color_order = dc.color_order + ['red']
    print(dc.color_order)


def yellow_pressed(dc):
    dc.color_order = dc.color_order + ['yellow']
    print(dc.color_order)


def enter_pressed(dc):
    for k in range(len(dc.color_order)):
        print(dc.color_order[k])
    dc.color_order = []


main()
