import psutil
import sys
import urllib.request #파이썬3에서
import threading
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
import pymongo
import subprocess


# apiKey = 'thingSpeak api-key for reading'
# baseURL = 'https://api.thingspeak.com/update?api_key='+apiKey+'&field1='

MONGO_HOSTNAME = '192.168.0.243'
MONGO_PORT = '27017'
MONGO_DB = 'wasp'

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        subprocess.run(["chmod", "+x", "src/angel_ss/docker_pull.sh"])
        print("dd")
        self.client = pymongo.MongoClient('mongodb://'+MONGO_HOSTNAME+':'+MONGO_PORT)
        self.subscription = self.create_subscription(
            Bool,
            '/topic/button/emr/bool',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        db = self.client.wasp.button
        button_db = {"id" : "M30", "buttonstate" : msg.data}
        db.insert(button_db)
        if msg.data == True :
            collection = self.client.wasp.updatebutton
            update_button = collection.findOne().sort({'_id':-1}).limit(1)
            if update_button.data == True :
                subprocess.run(["src/angel_ss/docker_pull.sh", "arguments"], shell=True)
    
        self.get_logger().info('I heard: "%s"' % msg.data)

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