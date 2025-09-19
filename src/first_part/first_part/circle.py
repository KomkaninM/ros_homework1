import rclpy
from std_msgs.msg import Float64
from rclpy.node import Node

from geometry_msgs.msg import Twist

class sendVelocity(Node) :
    def __init__(self):
        super().__init__('turtle_move')
        self.publisher_ = self.create_publisher(Twist,'/turtle1/cmd_vel',15)
        commRate = 1
        self.timer = self.create_timer(commRate, self.moveTurtle)
    
    def moveTurtle(self):
        msgPublish = Twist()
        msgPublish.linear.x = 2.0
        msgPublish.linear.y = 0.0
        msgPublish.linear.z = 0.0

        msgPublish.angular.x = 0.0
        msgPublish.angular.y = 0.0
        msgPublish.angular.z = 2.0

        self.publisher_.publish(msgPublish)


#Main Function
def main(args=None):
    rclpy.init(args=args)

    turtle_move = sendVelocity()
    rclpy.spin(turtle_move)
    
    turtle_move.destroy_node()
    rclpy.shutdown()

    
if __name__ == '__main__':
    main()
