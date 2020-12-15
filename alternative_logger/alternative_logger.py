#coding=utf8
import rclpy
import time
import os
import pickle
import ruamel.yaml as yaml

from marker_msgs.msg import _euler

from ament_index_python.packages import get_package_share_directory
from rosidl_runtime_py import utilities
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data


writing_txt = True


class Topic_example(Node):
    def __init__(self, topic_name, type, static_data_time):
        self.topic_name = topic_name
        self.type = type
        self.static_data_time = static_data_time
        print("topic %s init witch type %s" % (self.topic_name, self.type))

        self._topic_name_copy = self.topic_name
        self._topic_name_copy = self._topic_name_copy.replace('/', '_')

    def _write_file(self, data, file_name, time_msg):
        folder_name = str(self.static_data_time) + "_yaml"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        #===#
        cleen_dir_attr = []
        dirty_dir_attr = dir(data)
        for i in dirty_dir_attr:
            if not '__' in i and not i.isupper():
                cleen_dir_attr.append(i)

        dict_attrs = {}
        for n in cleen_dir_attr:
            attr = getattr(data, n)
            # print(attr)
            dict_attrs.update({'&\'%s' % n: attr})

        if writing_txt:
            print(time.time(), dict_attrs)
            with open('{0}/{1}.txt'.format(os.getcwd() + "/" + folder_name, self.static_data_time + file_name), 'a') as file:
                file.write('{}:{}\n'.format(time.time(), str(dict_attrs)))
        else:
            file = open('{0}/{1}.yaml'.format(os.getcwd() + "/" + folder_name, self.static_data_time + file_name), 'a')
            yaml.dump({"%s" % time.time(): dict_attrs}, file, default_flow_style=False, allow_unicode=True)
            file.close()


        #=#
        # file = open('{0}/{1}.txt'.format(os.getcwd() + "/" + str(self.static_data_time), self.static_data_time + file_name), 'a')
        # file.write('\n{0}'.format("<--" + time_msg + "-->"))
        # file.write('\n{0}'.format(data))
        # file.close()
        #=#

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


        self._write_file(msg, self._topic_name_copy, time.time())


class alternative_logger(Node):
    def __init__(self, node_name):
        self.node_name = node_name
        super().__init__(self.node_name)
        self.get_logger().info("init node with name: %s" % self.node_name)

        static_time = time.localtime(time.time())
        str_time_for_name_file = str(static_time.tm_mday) + "." + str(static_time.tm_mon) + "." + str(static_time.tm_year) + "-" + str(static_time.tm_hour) + ":" + str(static_time.tm_min) + ":" + str(static_time.tm_sec)
        print("Time: " + str_time_for_name_file)

        time.sleep(0.2)
        # получаем список существующих топиков и их типов
        self.list_topics = self.get_topic_names_and_types()

        sensor_msgs/msg/Imu

        geometry_msgs/msg/Euler

        geometry_msgs/msg/Euler



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
