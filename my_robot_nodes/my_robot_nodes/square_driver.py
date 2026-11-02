import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor

from lab_interfaces.action import DriveDistance, Rotate


class SquareDriver(Node):
    def __init__(self):
        super().__init__('square_driver')

        self.drive_client = ActionClient(
            self, DriveDistance, '/drive_distance'
        )
        self.rotate_client = ActionClient(
            self, Rotate, '/rotate'
        )

    def run_square(self):
        self.get_logger().info('Waiting for action servers...')

        self.drive_client.wait_for_server()
        self.rotate_client.wait_for_server()

        for side in range(4):
            self.get_logger().info(f'Side {side + 1}: Driving forward 1 metre')

            drive_goal = DriveDistance.Goal()
            drive_goal.distance = 1.0

            drive_future = self.drive_client.send_goal_async(drive_goal)
            rclpy.spin_until_future_complete(self, drive_future)

            drive_handle = drive_future.result()
            if not drive_handle or not drive_handle.accepted:
                self.get_logger().error('Drive goal rejected')
                return

            result_future = drive_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)

            drive_result = result_future.result().result
            if not drive_result.reached:
                self.get_logger().error('Drive failed or was interrupted')
                return

            self.get_logger().info(f'Side {side + 1}: Rotating 90 degrees')

            rotate_goal = Rotate.Goal()
            rotate_goal.angle = math.pi / 2

            rotate_future = self.rotate_client.send_goal_async(rotate_goal)
            rclpy.spin_until_future_complete(self, rotate_future)

            rotate_handle = rotate_future.result()
            if not rotate_handle or not rotate_handle.accepted:
                self.get_logger().error('Rotation goal rejected')
                return

            rotate_result_future = rotate_handle.get_result_async()
            rclpy.spin_until_future_complete(self, rotate_result_future)

            rotate_result = rotate_result_future.result().result
            if not rotate_result.success:
                self.get_logger().error('Rotation failed')
                return

        self.get_logger().info('Square completed successfully!')


def main(args=None):
    rclpy.init(args=args)
    node = SquareDriver()

    try:
        node.run_square()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
