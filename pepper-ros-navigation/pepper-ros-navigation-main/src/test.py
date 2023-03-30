#!/usr/bin/env python
import rospy 
import os
import sys
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import json
import time

rospy.init_node("test", anonymous=True)
client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
while not client.wait_for_server():
  print("try to connect to move_base server")
print("connected!")