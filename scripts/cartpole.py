#!/usr/bin/env python
#encoding: utf8
import rospy, unittest, rostest
import rosnode
from std_msgs.msg import Int16
from pfoe_cartpole.msg import CartPoleValues
import time
import gym

def recv_cmd_vel(control):
    rospy.loginfo(type(control))
    rospy.loginfo("%s", control.data)

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
            print("\nobservation", observation)
            print("\nreward = ", reward)
            print("\ndone = ", done)
            print("\ninfo", info)

class EnvCartPole:
    def __init__(self):
        self.env = gym.make("CartPole-v0")
        self.env_reset()
        self.pub = rospy.Publisher("cartpole_state", CartPoleValues, queue_size=10)

    def env_reset(self):
        self.observation = self.env.reset()
        print("#########################################################")
        print("To control this Cart, push Right-arrow or Left-arrow key.")
        print("\nWhen Cart_position increase or decreace over 2.4")
        print("   or Pole_angle Tilt over 20.9 deg,")
        print("   CartPole is Failure (Done is True).")
        print("#########################################################")
        self.step = 0

    def do_cartpole(self, linear):
        self.env.render()
        time.sleep(0.1)
        action = linear.data
        self.observation, self.reward, self.done, self.info = self.env.step(action)
        data = CartPoleValues()
        data.cart_position = self.observation[0]
        data.cart_velocity = self.observation[1]
        data.pole_angle = self.observation[2]
        data.pole_angular= self.observation[3]
        data.reward = self.reward
        data.done = self.done
        self.pub.publish(data)
        if self.done or self.step > 200:
            print("Episode finished after {} timesteps.".format(self.step + 1))
            print("Restart CartPole...")
            self.env_reset()
        else:
            print("cart_position = ", data.cart_position)
            print("cart_velocity = ", data.cart_velocity)
            print("pole_angle    = ", data.pole_angle)
            print("pole_angular  = ", data.pole_angular)
            self.step += 1
#        print("\nobservation = ", self.observation)
#        print("\nreword = ", self.reward)
#        print("\ndone = ", self.done)
#        print("\ninfo = ", self.info)
#        return self.obserbation, self.reward, self.done, self.info

def main():
    rospy.init_node("cartpole")
#    if start_cartpole == :
#        cartpole = envCartPole()
#        start_cartpole = "true"
    cartpole = EnvCartPole()
    rospy.Subscriber("key_in", Int16, cartpole.do_cartpole)
    rospy.spin()

if __name__ == "__main__backup":
    rospy.init_node("cartpole")
#    envCartPole()
    pub = rospy.Publisher("cartpole_state", CartPoleValues, 10)
    rospy.Subscriber("key_in", Int16, recv_cmd_vel)
    rospy.spin()

if __name__ == "__main__":
    main()
