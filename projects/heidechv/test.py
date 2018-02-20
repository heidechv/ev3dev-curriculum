def find_color(self, color_sig, color):
    self.pixy.mode = color_sig
    x = self.pixy.value(1)
    turn_speed = 100

    while 150 < x < 170:
        if x < 150:
            self.turn_left(turn_speed)
        else:
            self.turn_right(turn_speed)

        time.sleep(0.25)

    self.stop()
    ev3.Sound.speak(color).wait()


bot.pixy.mode = "SIG1"
width = robot.pixy.value(3)
height = robot.pixy.value(4)

mqtt.send_message('print_2', [width, height])


def print_2(self, width, height):
    print('width: ', width)
    print('height: ', height)