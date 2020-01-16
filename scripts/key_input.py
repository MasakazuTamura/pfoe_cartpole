#!/usr/bin/env python
import sys,tty,termios
import rospy
from std_msgs.msg import Int16

file_directory = "/home/mt/work/pfoe_cartpole/key_log/"
file_name = "key_cmd_list"
file_extention = ".txt"
file_path = file_directory + file_name + file_extention

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
#            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get3():
    inkey = _Getch()
#    while not rospy.is_shutdown():
#        k = inkey()
#    if k!='':break
    k = inkey()
    if k == '\x1b[C':
        print("right")
        linear_x = 1
    elif k=='\x1b[D':
        print("left")
        linear_x = 0
    else:
        print("arrow key only")
        linear_x = -1
    return k, linear_x

def get1():
    inkey = _Getch()
#    while not rospy.is_shutdown():
#        k = inkey()
#    if k!='':break
    k = inkey()
    # ^[C or ^[D
    if k == '\x1b':
        for i in range(0, 2):
            k += inkey()
        if k == "\x1b[C":
#            print("right")
            linear_x = 1
        elif k == "\x1b[D":
#            print("left")
            linear_x = 0
        else:
#            print("right or left only")
            linear_x = -1
    # ^C
    elif k == "\x03":
#        print("ctrl+c key down")
        linear_x = -1
    # ^R
    elif k == "\x12":
#        print("ctrl+r key down")
        linear_x = -1
    # ^S
    elif k == "\x13":
#        print("ctrl+s key down")
        linear_x = -1
    # ^X
    elif k == "\x18":
#        print("ctrl+x key down")
        linear_x = -1
    else:
#        print("unknown command")
#        print("note: arrow key only")
        linear_x = -1
    return k, linear_x

if __name__ == '__main__':
    rospy.init_node("key_cmd")
    pub = rospy.Publisher("key_in", Int16, queue_size=1)
    key_cmd_list = []
    key_replay = False

    key_cmd = Int16()
    rate = rospy.Rate(8)
    while not rospy.is_shutdown():
        if key_replay:
            key_cmd.data = int(key_cmd_list.pop(0))
            print(key_cmd.data)
            pub.publish(key_cmd)
            if not len(key_cmd_list):
                key_replay = False
        else:
            keyevent, key_cmd.data = get1()
#            print(keyevent, key_cmd.data)
            # ^C
            if keyevent == "\x03":
                rospy.signal_shutdown("ctrl+c")
            # ^R
            elif keyevent == "\x12":
                with open(file_path, mode="r") as f:
                    key_cmd_list = [s.strip() for s in f.readlines()]
                key_replay = True
            # ^S
            elif keyevent == "\x13":
                with open(file_path, mode="w") as f:
                    f.write("\n".join(map(str, key_cmd_list)))
#                print("save key_cmd history as {}".format(file_path))
                key_cmd_list = []
            # ^X
            elif keyevent == "\x18":
                key_cmd_list = []
            elif not key_cmd.data < 0:
                key_cmd_list.append(key_cmd.data)
                pub.publish(key_cmd)

        rate.sleep()

