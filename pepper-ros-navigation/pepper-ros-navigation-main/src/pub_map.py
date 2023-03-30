#!/usr/bin/env python

import rospy
import sys
from std_msgs.msg import Int32

def talker():
    pub = rospy.Publisher('/map_info', Int32, queue_size=10) # topic name
    rospy.init_node('tester', anonymous=True) # node name
    message = int(sys.argv[1])  
    print('debug')
    print(sys.argv[1])  
    pub.publish(message)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
