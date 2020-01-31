#!/usr/bin/env python
#encoding: utf8
from __future__ import print_function
import rospy, unittest, rostest
import rosnode
from std_msgs.msg import Int16
from pfoe_cartpole.msg import CartPoleValues, ButtonValues
import time
import gym
from gym.envs.registration import register

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
#            print("\nobservation", observation)
#            print("\nreward = ", reward)
#            print("\ndone = ", done)
#            print("\ninfo", info)

register(
    id='CartPolePFoE-v0',
    entry_point='gym.envs.classic_control:CartPoleEnv',
    max_episode_steps=1000,
    reward_threshold=195.0,
)

class EnvCartPole:
    def __init__(self):
        self.pub = rospy.Publisher("cartpole_state", CartPoleValues, queue_size=1)
        self.pub_result = rospy.Publisher("time_per_time", Int16, queue_size=10)    #csv出力用
        rospy.Subscriber("/key_in", Int16, self.cmdvel_callback)
        rospy.Subscriber("/buttons", ButtonValues, self.button_callback)
        self.make_env("CartPolePFoE-v0")
        self.env.seed(0)
        self.env_reset()

        self.front_toggle = False
        self.mid_toggle = False
        self.steps_threshold = 199

    def make_env(self, env_id):
        self.env = gym.make(env_id)

    def env_reset(self):
        print("\r#########################################################")
        print("\rTo control this Cart, push Right-arrow or Left-arrow key.")
        print("\rWhen Cart_position is more than +-2.4,")
        print("\r   Pole_angle is more than +-12 deg,")
        print("\r   or Episode_length is greater than 200,")
        print("\r   CartPole is Failure (Done is True).")
        print("\r#########################################################")
        #self.env.seed(0)
        self.observation = self.env.reset()
        self.env.render()
        self.reward = 0.0
        self.done = False
        self.step = 0
        self.input_keycmd = False
        self._print_state()
        self._publish_state()
        self.stopper = False

    def _publish_state(self):
        data = CartPoleValues()
        data.cart_position = self.observation[0]
        data.cart_velocity = self.observation[1]
        data.pole_angle = self.observation[2]
        data.pole_angular= self.observation[3]
        data.reward = self.reward
        data.done = self.done
        self.pub.publish(data)

    def _print_state(self):
        print("\r----------------")
        print("\r{} timesteps.".format(self.step))
        print("\rcart_position = ", self.observation[0])
        print("\rcart_velocity = ", self.observation[1])
        print("\rpole_angle    = ", self.observation[2])
        print("\rpole_angular  = ", self.observation[3])
        print("\rdone  = ", self.done)

    def _print_result(self):
        print("\r----------------")
        print("\rEpisode finished after {} timesteps.".format(self.step))
        print("\rRestart CartPole...")

    def button_callback(self, msg):
        if not msg.front_toggle == self.front_toggle:
            self.front_toggle = msg.front_toggle
            if self.front_toggle:
                self.steps_threshold = 999
                self.env.seed(0)
                self.env_reset()
            else:
                self.steps_threshold = 199
                time.sleep(1.0)
                self.env.seed(0)
                self.env_reset()

        if not msg.mid_toggle == self.mid_toggle:
            self.mid_toggle = msg.mid_toggle
            if self.mid_toggle:
                #self.env.seed(0)
                self.env_reset()

    def action_cartpole(self, linear_x):
        self.step += 1
        time.sleep(0.1)
        action = linear_x.data
        self.observation, self.reward, self.done, self.info = self.env.step(action)
        self._publish_state()
        self._print_state()
        if self.done:
            print("\rFailuer!")
        if self.done or self.step > self.steps_threshold:
            self.pub_result.publish(self.step)
            self._print_result()
            if self.mid_toggle == True:
                while self.mid_toggle:
                    time.sleep(0.1)
                while not self.mid_toggle:
                    time.sleep(1.0)
            time.sleep(1.0)
            self.env_reset()
        else:
            self.env.render()
#        return self.obserbation, self.reward, self.done, self.info

    def cmdvel_callback(self, linear_x):
        self.action = linear_x.data
        self.input_keycmd = True

    def run(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            if self.input_keycmd and not self.stopper:
                #time.sleep(0.1)
                self.step += 1
                self.observation, self.reward, self.done, self.info \
                = self.env.step(self.action)
                self.env.render()
                self._print_state()
                if self.done or self.step > self.steps_threshold:
                    self.stopper = True
                    if self.step < 200:
                        print("\rFailuer")
                    self._print_result()
                    self.done = True
                    self.pub_result.publish(self.step)
                    self.input_keycmd = False
                    self._publish_state()
                    if not self.mid_toggle:
                        time.sleep(1.0)
                        self.env.seed(0)
                        self.env_reset()
                else:
                    self.input_keycmd = False
                    self._publish_state()

            rate.sleep()

def main():
    cartpole = EnvCartPole()
    rospy.Subscriber("/key_in", Int16, cartpole.action_cartpole)
    rospy.spin()

if __name__ == "__main__backup":
    rospy.init_node("cartpole")
#    envCartPole()
    pub = rospy.Publisher("cartpole_state", CartPoleValues, 10)
    rospy.Subscriber("key_in", Int16, recv_cmd_vel)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("cartpole")
    EnvCartPole().run()
