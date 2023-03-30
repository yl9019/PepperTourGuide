#!/usr/bin/env python

import rospy
import time
import subprocess
from std_msgs.msg import String
from std_msgs.msg import Int32

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard a rumour that u said number %s', data.data)

    if (data.data == 2):    
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map2floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 6")
    elif (data.data == 1):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map1floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")
    elif (data.data == 3):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map3floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")
    elif (data.data == 4):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map4floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")
    elif (data.data == 5):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map5floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")
    elif (data.data == 6):
        #command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map6floor.yaml"
        command = "roslaunch pepper-ros-navigation nav6.launch"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")  
    elif (data.data == 5):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map7floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 7")
    elif (data.data == 8):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map8floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 8")
    elif (data.data == 9):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map9floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 9")
    elif (data.data == 10):
        #command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map10floor.yaml"
        command = "roslaunch pepper-ros-navigation nav6.launch"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 10")
    elif (data.data == 11):
        command = "rosrun map_server map_server ~/catkin_ws/src/pepper-ros-navigation/launch/maps/map11floor.yaml"
        ret = subprocess.check_output(command, shell=True)
        rospy.loginfo("publish map 10")
    else:
        print('not known floor')
    print(data.data)

def listener():
    rospy.init_node('floor_listener', anonymous=True)
    rospy.Subscriber('/map_info', Int32, callback)
    time.sleep(10)
    rospy.spin()

if __name__ == '__main__':
    listener()
