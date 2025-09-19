import rclpy
from std_msgs.msg import Float64, Float32
from rclpy.node import Node
from rclpy.action import ActionClient
import math
import time

from geometry_msgs.msg import Twist
from turtlesim.action import RotateAbsolute


class moveTriangle(Node):
    def __init__(self):
        super().__init__('turtle_move_triangle')

        # nontrie@DESKTOP-MF44Q0U:~$ ros2 action info -t /turtle1/rotate_absolute
        # Action: /turtle1/rotate_absolute -> Name : "/turtle1/rotate_absolute"
        # Action clients: 0
        # Action servers: 1
        #     /turtlesim [turtlesim/action/RotateAbsolute] -> Action : turtlesim.action.RotateAbsolute

        self.rotate_ = ActionClient(self, RotateAbsolute,"/turtle1/rotate_absolute" )   #ActionClient(self, Action, Name)
        self.publisher_ = self.create_publisher(Twist,'/turtle1/cmd_vel',15)

    def moveStraight(self,duration = 2.0, speed = 4.0) :
        msgPublish = Twist()
        msgPublish.linear.x = speed
        self.publisher_.publish(msgPublish)
        time.sleep(duration)

    def rotate(self, angle_input) :
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = angle_input

        self.rotate_.wait_for_server()
        goal_future = self.rotate_.send_goal_async(goal_msg)

        rclpy.spin_until_future_complete(self, goal_future)
        goal_handle = goal_future.result()

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)


#Main Function
def main(args=None):

    pi = math.pi

    rclpy.init(args=args)

    turtle_move = moveTriangle()

    turtle_move.rotate(0.0)
    turtle_move.moveStraight()
    turtle_move.rotate(2*pi/3)
    turtle_move.moveStraight()
    turtle_move.rotate(4*pi/3)
    turtle_move.moveStraight()

    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
