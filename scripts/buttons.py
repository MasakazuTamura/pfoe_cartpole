#!/usr/bin/env python
import rospy
from pfoe_cartpole.msg import ButtonValues

def get_state():
    state = rospy.get_param("console", "wait")
    try:
        if state in ["wait", "teach", "replay"]:
            raise Exception("unknown state")
    except Exception as error:
        rospy.logger("Value error: ", error)
        state = "wait"

    return state

if __name__ == "main":
    rospy.init_node("buttons")
    pub = rospy.Publisher("buttons", ButtonValues, queue_size=5)

    rate = rospy.Rate(10)
    msg = ButtonValues
    while not rospy.is_shutdown():
        s = get_state()
        if s != state:
            state = s

            if state == "wait":
                msg.front_toggle = False
                msg.mid_toggle = True
            elif state == "teach":
                msg.front_toggle = True
                msg.mid_toggle = False
            elif state == "replay":
                msg.front_toggle = False
                msg.mid_toggle = True

            pub.publish(msg)

        rate.sleep()
