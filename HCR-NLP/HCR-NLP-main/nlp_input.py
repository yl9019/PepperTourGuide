import rospy
from std_msgs.msg import String
import time
def talk2(str_msg,topic):
    pub = rospy.Publisher(topic, String, queue_size=10)
    rospy.init_node('nlp_node', anonymous=True)
    rospy.loginfo(str_msg)
    pub.publish(str_msg)

if __name__ == '__main__':
    while True:
        print("please input your question:")
        question = " "
        question = input("Question: ")
        print("Human: " + question)
        talk2(question,'nlp_input')