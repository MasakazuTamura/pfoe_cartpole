#!/usr/bin/env python
import sys,tty,termios
import rospy
from std_msgs.msg import Int16

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
    elif k == "\x03":
#        print("ctrl+c key down")
        linear_x = -1
    else:
#        print("unknown command")
#        print("note: arrow key only")
        linear_x = -1
    return k, linear_x

if __name__ == '__main__':
    rospy.init_node("key_cmd")
    pub = rospy.Publisher("key_in", Int16, queue_size=1)

    while not rospy.is_shutdown():
        key_cmd = Int16()
        keyevent, key_cmd.data = get1()
#        print(keyevent, key_cmd.data)
        if keyevent == "\x03":
            rospy.signal_shutdown("ctrl+c")
        if not key_cmd.data < 0:
            pub.publish(key_cmd)
