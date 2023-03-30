#!/usr/bin/env python

import rospy 
import os
import sys
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult, MoveBaseFeedback
from actionlib_msgs.msg import GoalStatus
import actionlib
import json
import time
import tf


class Communication:
    def __init__(self):
        rospy.init_node("communication", anonymous=True)
        self.rate = rospy.Rate(1)
        self.current_floor = None
        self.target_loc = None
        self.target_floor = None
        self.lift_door = None

        # Define the move_base actionlib properties
        self.goal = MoveBaseGoal()
        
        # Define the state of the navigation ['approaching_target', 'approaching_lift', 'wait_for_lift', 'inside_lift', 'outside_lift', 'goal_reached']
        # Define the state of movement using GoalStatus from the actionlib
        self.movement_state = None
        self.navigation_state = None

        # Define state message of type MoveBase
        # Define feedback messsage of type MoveBaseFeedback
        # Define result message of type MoveBaseResult     
        
        # self.result = None
        self.feedback = None
        self.state = None

        self.fake_result = None
        

                
        # self.goal = PoseStamped()
        self.lift_move = PoseStamped()  
        self.velocity = Twist()
        self.move_base_client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        self.move = PoseStamped()
        
        # Wait for the action server to come up
        rospy.loginfo("Waiting for the move_base action server...")
        # self.move_base_client.wait_for_server(rospy.Duration(3.0))
        rospy.loginfo("Server is started: %s", str(self.move_base_client.wait_for_server()))

        # get the result from the action server
        # self.result = self.move_base_client.get_result()
        
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 5)
        self.movement_pub = rospy.Publisher('/movement_state', String, queue_size = 5)
        self.lift_move_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 5)
        self.nlp_pub = rospy.Publisher('/nlp_input', String, queue_size = 5)
        # self.move_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 5)

        """TODO subscribe from move_base to check the status, like got plan or goal reached"""

        self.map = None
        with open('/root/catkin_ws/src/pepper-ros-navigation/src/map_location.json') as f:
            self.locations = json.loads(f.read())
        # print(self.locations)
        rospy.Subscriber('/current_floor', Int32, self.current_floor_callback)
        rospy.Subscriber('/target', String, self.target_location_callback, self.locations)
        rospy.Subscriber('/lift_door', String, self.lift_door_callback)
        # rospy.Subscriber('/fake_status', Int32, self.fake_status_callback)
        rospy.Subscriber('/goal_cancel', String, self.goal_cancel_callback)
        # subscribe to the topic if the user want to navigate to a new place after reached the previous goal

    def current_floor_callback(self, data):
        self.current_floor = data.data
        # print("The current floor number is {}".format(self.current_floor))
        rospy.loginfo(rospy.get_caller_id() + 'The current floor number: %s', str(self.current_floor))

    def target_location_callback(self, data, args):
        self.map = args
        rospy.loginfo("I heard %s",data.data)
        self.target_floor = int(data.data[:2])
        self.target_loc = self.map[data.data]
        rospy.loginfo(rospy.get_caller_id() + 'Target Floor: %s', str(self.target_floor))
        rospy.loginfo(rospy.get_caller_id() + 'Target Location: %s', str(self.target_loc))

    def lift_door_callback(self, data):
        self.lift_door = data.data
        rospy.loginfo(rospy.get_caller_id() + 'lift_door: %s', str(self.lift_door))

    def fake_status_callback(self, data):
        self.fake_result = data.data
        rospy.loginfo(rospy.get_caller_id() + 'fake_result: %s', str(self.fake_result))

    def goal_cancel_callback(self, data):
        if data.data == 'goal_cancel':
            self.move_base_client.cancel_goal()
            rospy.loginfo(rospy.get_caller_id() + 'The current goal is canceled')
        rospy.loginfo("wait for cancel result")
        self.state = self.move_base_client.get_state()
        rospy.loginfo(rospy.get_caller_id() + 'the state of goal cancelled: %s',self.state)
        self.navigation_state = 'goal_canceled'

    # prepare the message send to move_base/goal
    def prepare_move_base_msg(self, x, y, a, frame_id):
        # Create a goal message
        self.goal.target_pose.header.frame_id = frame_id# "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Set the goal position and orientation
        self.goal.target_pose.pose.position.x = x
        self.goal.target_pose.pose.position.y = y
        quaternion = tf.transformations.quaternion_from_euler(0, 0, a)
        self.goal.target_pose.pose.orientation.x = quaternion[0]
        self.goal.target_pose.pose.orientation.y = quaternion[1]
        self.goal.target_pose.pose.orientation.z = quaternion[2]
        self.goal.target_pose.pose.orientation.w = quaternion[3]

        rospy.loginfo("Sending goal to move_base...")

    # prepare the message send to move_base_simple/goal
    def prepare_move_base_simple_msg(self, x, y, a):
        # Create a lift_move message
        self.lift_move.header.frame_id = "base_footprint"
        self.lift_move.header.stamp = rospy.Time.now()

        # Set the lift_move position and orientation
        self.lift_move.pose.position.x = x
        self.lift_move.pose.position.y = y
        quaternion = tf.transformations.quaternion_from_euler(0, 0, a)
        self.lift_move.pose.orientation.x = quaternion[0]
        self.lift_move.pose.orientation.y = quaternion[1]
        self.lift_move.pose.orientation.z = quaternion[2]
        self.lift_move.pose.orientation.w = quaternion[3]

        rospy.loginfo("Sending goal to move_base_simple...")

    def send_move_base_msg(self, location, orientation, frame_id):
        self.prepare_move_base_msg(location[0], location[1], orientation, frame_id)
        self.move_base_client.send_goal(self.goal)
        # self.move_pub.publish(self.move)
        # get the state message of the robot
        # rospy.loginfo("waiting for result")
        # # self.move_base_client.wait_for_result()
        # rospy.loginfo("get result")
        self.state = self.move_base_client.get_state()
        rospy.loginfo(rospy.get_caller_id() + 'state of move_base: %s', self.state)
        while self.state == actionlib.GoalStatus.PENDING:
            rospy.loginfo('server has received the request and is preparing to process the goal')
            self.state = self.move_base_client.get_state()
            if self.navigation_state == 'goal_canceled':
                print("break the while loop")
                break

        while self.state == actionlib.GoalStatus.ACTIVE:
            # self.feedback = self.move_base_client.get_feedback()
            # TODO add interrupt and display the message of feedback 
            rospy.loginfo(rospy.get_caller_id() + 'Moving to goal: %s', self.navigation_state)
            # update the state of the movement
            # self.move_base_client.wait_for_result()
            self.state = self.move_base_client.get_state()
            if self.navigation_state == 'goal_canceled':
                print("break the while loop")
                break
            time.sleep(1)
        # self.move_base_client.wait_for_result()
        rospy.loginfo(rospy.get_caller_id() + 'Status Inactive: %s', self.state)

        # display the state
        if self.state:
            if self.state == actionlib.GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
            elif self.state == actionlib.GoalStatus.PREEMPTED:
                rospy.logwarn("Goal preempted!")
            elif self.state == actionlib.GoalStatus.ABORTED:
                rospy.logwarn("Goal aborted!")
        else:
            rospy.logerr("No result received")

    def cmd_vel(self, x, y, z):
        self.velocity.linear.x = x
        self.velocity.linear.y = y
        self.velocity.angular.z = z

    
    def path_planning(self):
        previous_target_loc = None
        previous_current_floor = None
        nlp_goal_info = 'continue'
    
        while not rospy.is_shutdown():
            # publish the move_base message

            if (self.current_floor is not None and self.target_loc is not None): # and (self.current_floor != previous_current_floor or self.target_loc != previous_target_loc):
                # indicate some message is received, start navigation process
                
                # Get the result of the move_base, including proceeding, finish, etc. 
                # self.result = self.move_base_client.get_result()
                self.state = self.move_base_client.get_state()
                rospy.loginfo('Navigation state: %s', self.navigation_state)
                
                if self.navigation_state == None:
                    if self.current_floor == self.target_floor:
                        self.navigation_state = 'approaching_target'
                        rospy.loginfo('Navigation state: %s', self.navigation_state)
                        self.send_move_base_msg(self.target_loc, 1.0,'map')
                    else: 
                        self.navigation_state = 'approaching_lift'
                        rospy.loginfo('Navigation state: %s', self.navigation_state)
                        if self.current_floor < 10:
                            lift_name = "0" + str(self.current_floor) + "mlift"
                        elif self.current_floor == 10 or self.current_floor == 11:
                            lift_name = str(self.current_floor) + "mlift"
                        else:
                            rospy.logerr("Invalid current floor number")
                        self.send_move_base_msg(self.map[lift_name][:2], self.map[lift_name][2], 'map')
                    previous_target_loc = self.target_loc
                    
                    
                elif self.navigation_state == 'goal_reached' or self.navigation_state == 'goal_canceled':
                    if previous_target_loc != self.target_loc:
                        self.navigation_state = None
                
                
            
                elif self.navigation_state == 'approaching_target':
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    # if self.fake_result ==  3:
                    self.state = self.move_base_client.get_state()
                    if self.state == actionlib.GoalStatus.SUCCEEDED:
                        self.navigation_state = 'goal_reached'
                        self.nlp_pub.publish(nlp_goal_info)
                        

                elif self.navigation_state == 'approaching_lift':
                    # if self.fake_result == 3:
                    self.state = self.move_base_client.get_state()
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    if self.state == actionlib.GoalStatus.SUCCEEDED:
                        self.navigation_state = 'wait_for_lift'

                elif self.navigation_state == 'wait_for_lift': 
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    if self.lift_door == 'open':
                        
                        # use move_base_simple to move pepper in the lift and turn around
                        # self.prepare_move_base_simple_msg(0.5, 0.0, 1.57)
                        # self.send_move_base_msg([0.5, 0.0, 3.14], 'base_footprint')
                        # self.lift_move_pub.publish(self.lift_move)
                        self.cmd_vel(0.0, 0.0, 0.8)
                        self.cmd_vel_pub.publish(self.velocity)
                        time.sleep(4)
                        self.cmd_vel(-0.8, 0.0, 0.0)
                        self.cmd_vel_pub.publish(self.velocity)
                        time.sleep(8)
                        self.cmd_vel(0.0, 0.0, 0.0)
                        self.cmd_vel_pub.publish(self.velocity)
                        self.navigation_state = 'entering_lift'
                        time.sleep(5)

                elif self.navigation_state == 'entering_lift':
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    self.state = self.move_base_client.get_state()
                    if self.lift_door == 'closed' and self.state == actionlib.GoalStatus.SUCCEEDED:
                        self.navigation_state = 'inside_lift'

                elif self.navigation_state == 'inside_lift':
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    if self.lift_door == 'open':
                        
                        # self.send_move_base_msg([0.5, 0.0, 0], 'base_footprint')
                        # self.lift_move_pub.publish(self.lift_move)
                        self.cmd_vel(0.0, 0.0, 0.8)
                        self.cmd_vel_pub.publish(self.velocity)
                        time.sleep(4)
                        self.cmd_vel(-0.8, 0.0, 0.0)
                        self.cmd_vel_pub.publish(self.velocity)
                        time.sleep(8)
                        # self.cmd_vel(0.0, 0.0, -0.8)
                        # self.cmd_vel_pub.publish(self.velocity)
                        # time.sleep(4)
                        self.cmd_vel(0.0, 0.0, 0.0)
                        self.cmd_vel_pub.publish(self.velocity)
                        self.navigation_state = 'exiting_lift'
                        time.sleep(4)
                
                elif self.navigation_state == "exiting_lift":
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    self.state = self.move_base_client.get_state()
                    if self.state == actionlib.GoalStatus.SUCCEEDED:
                        self.navigation_state = 'outside_lift'

                elif self.navigation_state == 'outside_lift':
                    rospy.loginfo('Navigation state: %s', self.navigation_state)
                    while self.current_floor != self.target_floor:
                        rospy.loginfo('Waiting for computer vision to confirm the floor number')
                        time.sleep(3)                   
                    self.send_move_base_msg(self.target_loc, 'base_footprint')
                    self.navigation_state = 'approaching_target'
                

                self.movement_pub.publish(self.navigation_state)
                


                # self.velocity.linear.x = 0.8
                # self.velocity.linear.y = 0.8
                # self.cmd_vel_pub.publish(self.velocity)
            
            # state = self.move_base_client.get_state()
            # rospy.loginfo(state)
            # previous_current_floor = self.current_floor
            # previous_target_loc = self.target_loc

            self.rate.sleep()

    
    def run(self):
        self.path_planning()
        rospy.spin()
            
        
if __name__ == "__main__":
    try: 
        robot_controller = Communication()
        robot_controller.run()
    except rospy.ROSInterruptException:
        pass