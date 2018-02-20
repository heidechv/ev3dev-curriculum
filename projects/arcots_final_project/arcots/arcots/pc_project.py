import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def press(mqtt_client):
    print('arrive')
    mqtt_client.send_message('chase_the_ball')


# def start_program(mqtt_client):
#     mqtt_client.open()


def quit_program(mqtt_client):
    mqtt_client.send_message('')
    exit()


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title = "Master Controller"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    spin_button = ttk.Button(main_frame, text="Spin")
    spin_button.grid(row=3, column=2)
    spin_button["command"] = lambda: mqtt_client.send_message('spin_for_the_ball')

    chase_button = ttk.Button(main_frame,  text="Chase")
    chase_button.grid(row=3, column=3)
    chase_button["command"] = lambda: press(mqtt_client)

    root.mainloop()


main()
