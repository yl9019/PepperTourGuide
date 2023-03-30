import rospy
from std_msgs.msg import String
import threading
import time
import sys
class InfoGetter(object):
    def __init__(self):
        #event that will block until the info is received
        self._event = threading.Event()
        #attribute for storing the rx'd message
        self._msg = None

    def __call__(self, msg):
        #Uses __call__ so the object itself acts as the callback
        #save the data, trigger the event
        self._msg = msg
        self._event.set()

    def get_msg(self, timeout=None):
        print("waitting for msg:")
        """Blocks until the data is rx'd with optional timeout
        Returns the received message
        """
        self._event.wait(timeout)
        return self._msg
    def clear_event(self):
        self._event.clear()
        self._msg = None
    
# if __name__ == '__main__':
#     rospy.init_node('infoGetter', anonymous=True)
#     #Get the infol
#     ig = InfoGetter()
#     rospy.Subscriber('nlp_input', String, ig)
#     #ig.get_msg() Blocks until message is received
#     msg = ig.get_msg()
#     print(msg)
# def wait_trigger():
#     ig2 = InfoGetter()
#     rospy.Subscriber('trigger_detected', String, ig2)
#     print("waitting for trigger:")
#     msg2 = ig2.get_msg()
#     return str(msg2.data) 