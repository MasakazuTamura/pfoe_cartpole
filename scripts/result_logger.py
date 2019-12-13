#!/usr/bin/env python

from __future__ import print_function
import rospy
from std_msgs.msg import Int16
from pfoe_cartpole.msg import ButtonValues
import datetime
import csv

file_directory = "/home/mt/work/pfoe_cartpole/test_log/"
file_name = "replay_"
file_extention = ".csv"

class Logger():
    def __init__(self):
#        rospy.Subscriber("/buttons", ButtonValues, self.button_callback)
        rospy.Subscriber("/time_per_time", Int16, self.result_callback)
        self.replay = False
        self.gen_newfile = False
        self.sub_newresult = False
        self.counter = 0

    def reset(self, console):
        if console == "wait":
#            print("\rwait")
            self.replay = False
            self.gen_newfile = False
            self.sub_newresult = False
        elif console == "replay" and self.replay == False:
#            print("\rreplay_start")
            self.replay = True
            self.gen_newfile = True
            self.counter = 0
#        elif console == "replay":
#            print("\rreplay")
#        else:
#            print("\rother")

    def run(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            self.reset(self.get_state())
            if self.replay == True:
                if self.gen_newfile == True:
                    self.generate_filename()
                    self.gen_newfile = False
                    print("\rgen_newfile:" + self.file_path)

                if self.sub_newresult == True:
                    self.write_row()
                    self.sub_newresult = False
                    self.counter += 1

                if self.counter >= 110:
                    self.gen_newfile = True
                    self.counter = 0

            rate.sleep()

    def generate_filename(self):
        datetime_now = datetime.datetime.now()
        self.file_path = file_directory + file_name + datetime_now.strftime("%Y%m%d%H%M") + file_extention
        with open(self.file_path, mode="w") as f:
            pass
#            writer = csv.writer(f)
#            writer.writerow([""])

    def write_row(self):
        with open(self.file_path, mode="a") as f:
            writer = csv.writer(f)
            writer.writerow([self.result])
            print("\rwriter: {}".format(self.result))

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


    def button_callback(self, button): #no use
        if button.mid_toggle == True:
            if self.replay == False:
                self.replay = True
                self.gen_newfile = True
        else:
            self.replay = False


    def result_callback(self, result):
        self.result = result.data
        print("\rget_result:{}".format(self.result))
        self.sub_newresult = True


if __name__ == "__main__":
    rospy.init_node("result_logger")
    Logger().run()
#    logger = Logger()
#    logger.generate_filename()
#    logger.result = "test"
#    logger.write_row()

