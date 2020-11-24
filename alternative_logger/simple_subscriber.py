import rclpy
from rclpy.node import Node
from marker_msgs.msg import LocalNav
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(LocalNav, '/rtp_1/local_nav', self.listener_callback, qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning
        print("OK")

    def listener_callback(self, msg):
        print("ok")
        self.get_logger().info(str(msg))

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()