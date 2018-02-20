import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

def start_program(mqtt_client):
    mqtt_client.open()


def quit_program(mqtt_client):
    mqtt_client.send_message('')
    exit()


robot = robo.Snatch3r()


mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()

root = tkinter.Tk()
root.title = "Master Controller"

main_frame = ttk.Frame(root, padding=5)
main_frame.grid()

canvas = tkinter.Canvas(main_frame, background="lightgray", width=320, height=200)
canvas.grid(columnspan=2)

rect_tag = canvas.create_rectangle(150, 90, 170, 110, fill="blue")

quit_button = ttk.Button(main_frame, text="Quit")
quit_button.grid(row=3, column=1)
quit_button["command"] = lambda: quit_program(mqtt_client)

spin_button = ttk.Button(main_frame, text="Spin")
spin_button.grid(row=3, column=2)
spin_button["command"] = lambda: ['spin_for_the_ball', [robot]]

chase_button = ttk.Button(main_frame,  text="Chase")
chase_button.grid(row=3, column=3)
chase_button["command"] = lambda: ['chase_the_ball', [robot]]

root.mainloop()


def spin_for_the_ball(self, robo):
    ev3.Sound.speak('Time to work my obliques').wait()
    while True:
        pixy_x = robo.get_pixy_x()
        print(pixy_x)
        if pixy_x is None:
            robo.drive(30, -30)
        elif pixy_x < 140:
            robot.drive(-30, 30)
        elif pixy_x > 170:
            robot.drive(30, -30)
        else:
            robot.stop()
            ev3.Sound.speak('I am tired')


def chase_the_ball(robot):
    ev3.Sound.speak('Time for some cardio').wait()
    while True:
        front_sensor = robot.get_front_proximity_sensor_reading()
        print(front_sensor)
        if front_sensor < 420:
            robot.start_moving(40, 40)
        elif front_sensor > 550:
            robot.stop_moving()
        else:
            robot.stop_moving()
            ev3.Sound.speak('I am tired')

