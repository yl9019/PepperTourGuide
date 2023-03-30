#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import json
import time
import sys
import os

class FloorPublisher:
    def __init__(self):
        rospy.init_node('floor_publisher')
        self.floor_pub = rospy.Publisher('/current_floor', Int32, queue_size=10)
        self.rate = rospy.Rate(0.5) # publish once per two second
        self.file_path = '/pepper_project/CV/intel/text.json' # replace with your own file path
        self.data = None
        self.load_json_data()
        self.previous_floor = None
        self.floor = 0
        self.run()

    def load_json_data(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def run(self):
        while not rospy.is_shutdown():
            if int(time.time()) % 5 == 0:
                self.load_json_data()
                self.previous_floor = self.floor
                self.floor = self.data.get('text', 0)
                # os.system('python ~/catkin_ws/src/pepper-ros-navigation/src/pub_map.py '+ str(self.floor))
                if self.previous_floor != self.floor:
                    os.system('python ~/catkin_ws/src/pepper-ros-navigation/src/pub_map.py '+ str(self.floor)) # this is for map changing
                    print("sending message")
                    self.floor_pub.publish(int(self.floor))
                    rospy.loginfo(rospy.get_caller_id() + 'The current floor number %s', str(self.floor))
                self.rate.sleep()
        rospy.spin()

if __name__ == '__main__':
    try:
        floor_publisher = FloorPublisher()
    except rospy.ROSInterruptException:
        pass
