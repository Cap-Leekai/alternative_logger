#coding=utf8
import rclpy
import time

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from marker_msgs.msg import *
from sensor_msgs.msg import Imu

rtp_id = 1

class Topic_example(Node):
    def __init__(self, topic_name, type, data_time):
        self.topic_name = topic_name
        self.type = type
        self.data_time = data_time
        print("topic %s init witch type %s" % (self.topic_name, self.type))

        self.topic_name_copy = self.topic_name
        # print("topic_name: ", self.topic_name)
        self.topic_name_copy = self.topic_name_copy.replace('/', '_')
        # print("as", self.topic_name_copy)

    def write_file(self, data, file_name, time_msg):
        file = open('{0}.txt'.format(self.data_time + file_name), 'a')
        file.write('\n{0}'.format("<--" + time_msg + "-->"))
        file.write('\n{0}'.format(data))
        file.close()

    def topic_cb(self, msg):
        """
        :param msg:
        :return: nothing
        cb. is writing msg to file
        """
        dynamic_time = time.localtime(time.time())

        str_time_for_msg = str(dynamic_time.tm_mday) + "." + str(dynamic_time.tm_mon) + "." + str(
            dynamic_time.tm_year) + "-" + str(dynamic_time.tm_hour) + ":" + str(dynamic_time.tm_min) + ":" + str(
            dynamic_time.tm_sec)

        print(dir(msg))

        self.write_file(msg, self.topic_name_copy, str_time_for_msg)


class alternative_logger(Node):
    def __init__(self, node_name):
        self.node_name = node_name
        super().__init__(self.node_name)
        self.get_logger().info("init node with name: %s" % self.node_name)
        static_time = time.localtime(time.time())

        str_time_for_name_file = str(static_time.tm_mday) + "." + str(static_time.tm_mon) + "." + str(static_time.tm_year) + "-" + str(static_time.tm_hour) + ":" + str(static_time.tm_min) + ":" + str(static_time.tm_sec)

        print("Time: " + str_time_for_name_file)

        #initing topic examples
        topic1 = Topic_example("/rtp_%s/local_nav" % rtp_id, LocalNav, str_time_for_name_file)
        topic2 = Topic_example("/rtp_%s/imu" % rtp_id, Imu, str_time_for_name_file)


        """
        concept:
        # Вместо инициализации топиков через кучу строк лучше будет сделать цикл for, 
        который будет перебирать список топиков и типов сообщений, для каждого топика соответственно, и уже в этом цикле делать создание сабскрайбера.
        Это позволит сделать инициализацию сабскрайберов динамическим и тогда программа будет подписываться на столько топиков, сколько указано в списке.
        
        for topic_and_type in topics_list:
            create subscriptions for topic_and_type
        
        """

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
