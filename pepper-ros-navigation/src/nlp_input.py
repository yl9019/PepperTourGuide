import rospy
from std_msgs.msg import String
import time
def talk(str,topic = 'nlp_input'):
    pub = rospy.Publisher(topic, String, queue_size=10)
    rospy.init_node('nlp', anonymous=True)
    rospy.loginfo(str)
    pub.publish(str)

if __name__ == '__main__':
    while True:
        print("please input your question:")
        question = " "
        question = input("Question: ")
        print("Human: " + question)
        talk("triggered by keyboard",topic='trigger_detected')
        # time.sleep(2)
        talk(question)