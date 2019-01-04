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
#            ch = sys.stdin.read(1)
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
#    while not rospy.is_shutdown():
#        k = inkey()
#    if k!='':break
    k = inkey()
    if k == '\x1b[C':
        print("right")
        linear = 1
    elif k=='\x1b[D':
        print("left")
        linear = 0
    else:
        print("arrow key only")
        linear = -1
    return k, linear

def main():
    for i in range(0,20):
        get()

if __name__ == '__main__':
    rospy.init_node("key_cmd")
    pub = rospy.Publisher("key_in", Int16, queue_size=1)

    while not rospy.is_shutdown():
        key_cmd = Int16()
        keyevent, key_cmd.data = get()
        print(keyevent, key_cmd.data)
        if not key_cmd.data < 0:
            pub.publish(key_cmd)
