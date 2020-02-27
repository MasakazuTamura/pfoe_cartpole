#!/usr/bin/env python
#encoding: utf8
from __future__ import print_function
import time
import gym

def envCartPole_sample():
    env = gym.make("CartPole-v0")

    for episode in range(20):
        observation = env.reset()                           #初期化
        for t in range(100):
            #action: left = 0, right = 1
            #obserbation: [cart位置 cart速度 pole角度 pole回転速度]
            env.render()
            action = env.action_space.sample()
            observation,reward,done,info = env.step(action) #cartに出力
            if done:
                print("Episode finished after {} timesteps.".format(t+1))
                break

            #棒が倒れている時: reward=0, done=True
            #棒が立っている時: reward=1, done=False
#            print("\nobservation", observation)
#            print("\nreward = ", reward)
#            print("\ndone = ", done)
#            print("\ninfo", info)

if __name__ == "__main__":
    envCartPole_sample()

