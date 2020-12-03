#coding=utf8
import rclpy
import time
import os

from rosidl_runtime_py import import_message_from_namespaced_type, utilities
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
#from ros2topic.api import get_msg_class


rtp_id = 1


class Topic_example(Node):
    def __init__(self, topic_name, type, static_data_time):
        self.topic_name = topic_name
        self.type = type
        self.static_data_time = static_data_time
        print("topic %s init witch type %s" % (self.topic_name, self.type))

        self._topic_name_copy = self.topic_name
        # print("topic_name: ", self.topic_name)
        self._topic_name_copy = self._topic_name_copy.replace('/', '_')
        # print("as", self.topic_name_copy)

    def _write_file(self, data, file_name, time_msg):
        if not os.path.isdir(str(self.static_data_time)):
            os.mkdir(str(self.static_data_time))
        # print(os.getcwd() + "/" + str(self.static_data_time))
        file = open('{0}/{1}.txt'.format(os.getcwd() + "/" + str(self.static_data_time), self.static_data_time + file_name), 'a')
        file.write('\n{0}'.format("<--" + time_msg + "-->"))
        file.write('\n{0}'.format(data))
        file.close()

    def _topic_cb(self, msg):
        """
        :param msg:
        :return: nothing
        cb. is writing msg to file
        """
        dynamic_time = time.localtime(time.time())

        dynamic_str_time_for_msg = str(dynamic_time.tm_mday) + "." + str(dynamic_time.tm_mon) + "." + str(
            dynamic_time.tm_year) + "-" + str(dynamic_time.tm_hour) + ":" + str(dynamic_time.tm_min) + ":" + str(
            dynamic_time.tm_sec)

        print(dir(msg))

        self._write_file(msg, self._topic_name_copy, dynamic_str_time_for_msg)


class alternative_logger(Node):
    def __init__(self, node_name):
        self.node_name = node_name
        super().__init__(self.node_name)
        self.get_logger().info("init node with name: %s" % self.node_name)

        static_time = time.localtime(time.time())
        str_time_for_name_file = str(static_time.tm_mday) + "." + str(static_time.tm_mon) + "." + str(static_time.tm_year) + "-" + str(static_time.tm_hour) + ":" + str(static_time.tm_min) + ":" + str(static_time.tm_sec)
        print("Time: " + str_time_for_name_file)

        # получаем список существующих топиков и их типов
        self.list_topics = self.get_topic_names_and_types()

        # creating topic objects
        topic_objects_list = []
        for topic in self.list_topics:
            topic_objects_list.append(Topic_example(topic[0], utilities.get_message(topic[1][0]), str_time_for_name_file))  # utilities.get_message(topic[1][0]): позволяет импортировать сообщение в код получая на вход его строковое название
        # print(topic_list)

        #initing subscriptions
        for topic in topic_objects_list:
            self.sub = self.create_subscription(topic.type, topic.topic_name, topic._topic_cb, qos_profile_sensor_data)
            self.sub


def main():
    rclpy.init()
    logger = alternative_logger("alternative_logger_node")

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
