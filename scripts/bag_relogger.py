#!/usr/bin/env python

from __future__ import print_function
import datetime
import csv
import sys
import numpy as np
import rosbag

#raspimouse_gamepad_teach_and_replay.msg Event
#   Event.cart_position
#   Event.cart_velocity
#   Event.pole_angle
#   Event.pole_angular
#   Event.linear_x

bag_directory = "/home/mt/.ros/"
bag_extention = ".bag"
relog_directory = "/home/mt/work/pfoe_cartpole/test_log/"
relog_name = "teach_"
relog_sim = "weights_"

def save_as_csv(array, directory, filename):
    filepath = directory + filename + ".csv"
    with open(filepath, mode="w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(array)
    print("save as \"{}\"".format(filepath))

def likelifood(past, last, func_type="diff"):
    if not past.shape[0] == last.shape[0]:
        raise IndexError("array size are not same size.")
    weight = 1.0
    for i in range(past.shape[0]):
        if func_type == "diff":
            difference = past[i] - last[i]
        elif func_type == "log":
            if past[i] * last[i] > 0:
                difference = np.log10(np.absolute(past[i])) - np.log10(np.absolute(last[i]))
            else:
                difference = past[i] - last[i]
        weight /= 1 + np.absolute(difference)
    return weight

if __name__ == "__main__":
    # get file name
    args = sys.argv
    try:
        print("Filename: {}{}".format(args[1], bag_extention))
        filename = args[1]
    except IndexError as e:
        print(e)
        print("Input bugfile-name: ")
        filename = str(raw_input())

    bag_filepath = bag_directory + filename + bag_extention


    # read bag file
    bag = rosbag.Bag(bag_filepath)
    episode = None
    for topic, msg, time in bag.read_messages():
        if topic == "/event":
            event = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0]])
            event[0, 0] = time.secs
            event[0, 1] = time.nsecs
            event[0, 2] = msg.cart_position
            event[0, 3] = msg.cart_velocity
            event[0, 4] = msg.pole_angle
            event[0, 5] = msg.pole_angular
            event[0, 6] = msg.linear_x
            if episode is None:
                episode = event
            else:
                episode = np.append(episode, event, axis=0)

    bag_size = episode.shape[0]


    # reshape time
    start_sec = episode[0,0]
    start_nsec = episode[0,1]
    re_time = np.zeros(bag_size, dtype="float32")
    for i in range(bag_size):
        re_time[i] = (episode[i, 0]-start_sec) + (episode[i, 1]-start_nsec)/1000000000.0


    # reshape episode
    re_episode = None
    for i in range(bag_size):
        re_event = np.zeros((1, 6), dtype="float32")
        re_event[0, 0] = re_time[i]
        re_event[0, 1] = episode[i, 2]
        re_event[0, 2] = episode[i, 3]
        re_event[0, 3] = episode[i, 4]
        re_event[0, 4] = episode[i, 5]
        re_event[0, 5] = episode[i, 6]
        if re_episode is None:
            re_episode = re_event
        else:
            re_episode = np.append(re_episode, re_event, axis=0)


    # relog as csv
    #save_as_csv(re_episode, relog_directory, relog_name + filename)
    #print("Save as {}.csv".format(relog_directory + relog_name + filename))


    # simulate weights
    try:
        function = args[2]
        if not function in ["diff", "log"]:
            raise ValueError("undefined function-type")
    except (IndexError, ValueError) as e:
        print(e)
        function = "diff"
        sensors = 4
    else:
        try:
            sensors = args[3]
        except IndexError as e:
            print(e)
            sensors = 4
    finally:
        print("Likelifood function-type: {}".format(function))
        print("Number of sensors: {}".format(sensors))

    weights = None
    start_point = 5 - sensors

    for i in range(bag_size):
        print(re_episode[0, start_point:5], re_episode[i, start_point:5])

"""
    for i in range(bag_size):
        weight = np.zeros((1, bag_size))
        for j in range(bag_size):
            weight[i, j] = likelifood(re_episode[j, start_point:5], re_episode[i, start_point:5], func_type=function)
        if weights is None:
            weights = weight
        else:
            weights = np.append(weights, weight, axis=0)

    print("Simulate weights")


    # weights as csv
    save_as_csv(weights, relog_directory, relog_sim + filename)
    print("Save as {}".format(relog_directory + relog_sim + filename))
"""
