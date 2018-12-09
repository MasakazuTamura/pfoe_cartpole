#!/usr/bin/env python
#encoding: utf8
import rospy, unittest, rostest
import rosnode
from std_msgs.msg import String
import time
import gym

def recv_key(control):
    rospy.loginfo(type(control))
    rospy.loginfo("%s", control.data)

def envCartPole():
    env = gym.make("CartPole-v0")

    for episode in range(20):
        observation = env.reset()                           #初期化
        for t in range(100):
            #action: left = 0, right = 1
            #obserbation: [cart位置 cart速度 pole角度 pole回転速度]
            env.render()
            print(observation)
            action = env.action_space.sample()
            observation,reward,done,info = env.step(action) #cartに出力
            if done:
                print("Episode finished after {} timesteps.".format(t+1))
                break

            #棒が倒れている時: reward=0, done=True
            #棒が立っている時: reward=1, done=False
            print("\nreward = ",reward)
            print("\ndone = ",done)
            print("\ninfo",info)

if __name__ == "__main__":
    rospy.init_node("cartpole")
#    envCartPole()
    sub = rospy.Subscriber("key_in", String, recv_key)
    rospy.spin()
