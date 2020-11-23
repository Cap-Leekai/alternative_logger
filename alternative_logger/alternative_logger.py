import rclpy
from rclpy.node import Node
from marker_msgs.msg import *

class Topic_exaple():
    def __init__(self, topic_name, type):
        self.topic_name = topic_name
        self.type = type
        print("topic %s init witch type %s" % (self.topic_name, self.type))

class alternative_logger(Node):
    def __init__(self, node_name):
        self.node_name = node_name
        super().__init__(self.node_name)
        self.get_logger().info("init node with name: %s" % self.node_name)
        self.list_topics = self.get_topic_names_and_types()

        print(self.list_topics)
        # импортируем типы сообщений для всех существующих топиков !Функция работает только для конструкции "пакет".msg!



def main():
    rclpy.init()

    logger = alternative_logger("alternative_logger_node")

if __name__ == "__main__":
    main()
