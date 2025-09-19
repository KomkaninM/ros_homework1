import rclpy
from std_msgs.msg import Float64, Float32
from rclpy.node import Node
from rclpy.action import ActionClient
import math
import time

from geometry_msgs.msg import Twist
from turtlesim.msg  import Pose
from turtlesim.action import RotateAbsolute

#x,y 0,0 to 11,11
class turtleMove(Node):
    def __init__(self, target_x, target_y):

        super().__init__('turtle_writing')

        self.rotate_ = ActionClient(self, RotateAbsolute,"/turtle1/rotate_absolute" )   #ActionClient(self, Action, Name)

        #use $ros2 topic list -t to find
        self.velocity_ = self.create_publisher(Twist,'/turtle1/cmd_vel',15)
        self.position_ = self.create_subscription(Pose,'/turtle1/pose',self.callback,15)

        self.target_x = target_x
        self.target_y = target_y
        self.dx = -1
        self.dy = -1
        self.angle_heading = -1.57
    
    def callback(self, position:Pose) :
        x = position.x
        y = position.y
        self.dx = self.target_x - x
        self.dy = self.target_y - y
        self.angle_heading = math.atan2(self.dy,self.dx)
        # self.get_logger().info(f"dx={self.dx:.2f}, dy={self.dy:.2f}, best_angle = {self.angle_heading:.2f}")


    def diffPosition(self):
        return abs(self.dx), abs(self.dy), self.angle_heading

    def moveStraight(self,duration = 0.05, speed = 3.0) :
        msgPublish = Twist()
        msgPublish.linear.x = speed
        self.velocity_.publish(msgPublish)
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

    rclpy.init(args=args)
    tol = 0.02
    speed_variable = 2.0

    K = [[2.0,2.0], [2.0,5.0], [4.0,8.0], [2.0,5.0], [4.0,2.0]] #Start at (2,8)

    for tx,ty in K :
        turtle = turtleMove(target_x=tx, target_y=ty)
        dx,dy,best_angle = turtle.diffPosition()
        max_dx = dx
        max_dy = dy
        while True:
            rclpy.spin_once(turtle,timeout_sec=0.025)
            dx,dy,best_angle = turtle.diffPosition()
            print(dx,dy,best_angle)
            if dx <= tol and dy <= tol:
                turtle.moveStraight(duration=0.0, speed=0.0)
                break
            elif(dx >= 0 and dy >= 0) :
                turtle.rotate(float(best_angle))
                turtle.moveStraight(duration = 0.02, speed = float(speed_variable))

    M = [[4.0,2.0],[5.0,8.0],[6.0,5.0],[7.0,8.0],[8.0,2.0]]
    for tx,ty in M :
        turtle = turtleMove(target_x=tx, target_y=ty)
        dx,dy,best_angle = turtle.diffPosition()
        max_dx = dx
        max_dy = dy
        while True:
            rclpy.spin_once(turtle,timeout_sec=0.025)
            dx,dy,best_angle = turtle.diffPosition()
            print(dx,dy,best_angle)
            if dx <= tol and dy <= tol:
                turtle.moveStraight(duration=0.0, speed=0.0)
                break
            elif(dx >= 0 and dy >= 0) :
                turtle.rotate(float(best_angle))
                turtle.moveStraight(duration = 0.02, speed = float(speed_variable))

    dx,dy,best_angle = turtle.diffPosition()
    print("Final Position")
    print(dx,dy,best_angle)

    turtle.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
