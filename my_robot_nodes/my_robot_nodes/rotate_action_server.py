import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from lab_interfaces.action import Rotate


class RotateActionServer(Node):
    def __init__(self):
        super().__init__('rotate_action_server')

        self.callback_group = ReentrantCallbackGroup()
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10,
            callback_group=self.callback_group
        )

        self.yaw = 0.0

        self.action_server = ActionServer(
            self,
            Rotate,
            'rotate',
            self.execute_callback
        )

        self.get_logger().info('Rotate action server started')

    def odom_callback(self, msg):
        q = msg.pose.pose.orientation

        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)

        self.yaw = math.atan2(siny, cosy)

    def execute_callback(self, goal_handle):
        target = goal_handle.request.angle
        start_yaw = self.yaw
        direction = 1.0 if target >= 0 else -1.0

        command = Twist()
        command.angular.z = direction * 0.4

        rate = self.create_rate(20)
        feedback = Rotate.Feedback()

        while rclpy.ok():
            traveled = direction * (self.yaw - start_yaw)
            traveled = abs(math.atan2(math.sin(traveled), math.cos(traveled)))

            remaining = abs(target) - traveled

            feedback.remaining_angle = max(0.0, remaining)
            goal_handle.publish_feedback(feedback)

            if traveled >= abs(target):
                break

            self.publisher.publish(command)
            rate.sleep()

        self.publisher.publish(Twist())

        goal_handle.succeed()

        result = Rotate.Result()
        result.success = True
        result.message = 'Rotation completed'

        return result


def main(args=None):
    rclpy.init(args=args)
    node = RotateActionServer()
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.remove_node(node)
        node.destroy_node()
        executor.shutdown()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
