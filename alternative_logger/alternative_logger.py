import rclpy
from rclpy.node import Node
from marker_msgs.msg import *
from rclpy import logging
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu

rtp_id = 1

class Topic_example(Node):
    def __init__(self, topic_name, type):
        self.topic_name = topic_name
        self.type = type
        print("topic %s init witch type %s" % (self.topic_name, self.type))

    def topic_cb(self, msg):
        """
        :param msg:
        :return: nothing
        cb. is writing msg to file
        """
        pass
        # print(msg)
        # self.get_logger().log(msg, Lo)

class alternative_logger(Node):
    def __init__(self, node_name):
        self.node_name = node_name
        super().__init__(self.node_name)
        self.get_logger().info("init node with name: %s" % self.node_name)

        #initing topic examples
        topic1 = Topic_example("/rtp_%s/local_nav" % rtp_id, LocalNav)
        topic2 = Topic_example("/rtp_%s/imu" % rtp_id, Imu)

        #initing subscriptions
        self.sub1 = self.create_subscription(topic1.type, topic1.topic_name, topic1.topic_cb, qos_profile_sensor_data)
        self.sub1
        self.sub2 = self.create_subscription(topic2.type, topic2.topic_name, topic2.topic_cb, qos_profile_sensor_data)
        self.sub2

def main():
    rclpy.init()
    logger = alternative_logger("alternative_logger_node")

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
