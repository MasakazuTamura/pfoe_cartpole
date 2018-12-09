#!/usr/bin/env python
import sys,tty,termios
import rospy
from std_msgs.msg import String

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
    if k=='\x1b[A':
        print("up")
    elif k=='\x1b[B':
        print("down")
    elif k=='\x1b[C':
        print("right")
    elif k=='\x1b[D':
        print("left")
    return k

def main():
    for i in range(0,20):
        get()

if __name__=='__main__':
    rospy.init_node("key_input")
    pub = rospy.Publisher("key_in", String, queue_size=10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        keyin = String()
        keyevent = get()
        keyin.data = keyevent
        print(keyevent, keyin.data)
        pub.publish(keyin)
        rate.sleep()
