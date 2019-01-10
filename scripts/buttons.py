#!/usr/bin/env python
from __future__ import print_function
import rospy
from pfoe_cartpole.msg import CartPoleValues, ButtonValues
import time

class Buttons():
    def __init__(self):
        self.pub = rospy.Publisher("buttons", ButtonValues, queue_size=5)
        rospy.Subscriber("cartpole_state", CartPoleValues, self.callback)

        self.msg = ButtonValues()
        self.state = "wait"
        self.state = self.get_state
        self.done = "replay"

    def run(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            s = self.get_state()
            replay_s = self.get_state_replay()
            if replay_s != self.state:
                self.state = replay_s

                if self.state == "replay":
                    if s == self.state:
                        print("\rconsole: change to \"replay\"")
                        self.msg.front_toggle = False
                        self.msg.mid_toggle = True
                    else:
                        self.state = s
                elif self.state == "wait":
                    print("\rconsole: change to \"wait\"")
                    self.msg.front_toggle = False
                    self.msg.mid_toggle = False
                elif self.state == "teach":
                    print("\rconsole: change to \"teach\"")
                    self.msg.front_toggle = True
                    self.msg.mid_toggle = False

                self.pub.publish(self.msg)
                time.sleep(5.0)

            rate.sleep()

    def get_state_replay(self):
        if self.state == "replay":
            console = self.done
        else:
            console = self.get_state()
        return console

    def get_state(self):
        console = rospy.get_param("console", "wait")
        try:
            if not console in ["wait", "teach", "replay"]:
                raise Exception("unknown state")
        except Exception as error:
#            rospy.logerr("Value error: ", error)
            print("\rValue error: {}".format(error))
            console = "wait"

        return console

    def callback(self, cartpolestate):
        if cartpolestate.done == True:
            self.done = "wait"
        else:
            self.done = "replay"

if __name__ == "__main__":
    rospy.init_node("buttons")
    Buttons().run()
