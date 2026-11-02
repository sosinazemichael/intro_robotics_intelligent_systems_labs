#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from lab_interfaces.msg import ObstacleInfo, RobotStatus
from lab_interfaces.srv import SetActive, SetSpeed


class TurnAway(Node):
    def __init__(self):
        super().__init__('turn_away')

        self.declare_parameter('forward_speed', 0.2)
        self.declare_parameter('turn_speed', 0.5)
        self.declare_parameter('max_turn_speed', 1.0)

        self.enabled = True

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_publisher = self.create_publisher(
            RobotStatus, '/robot_status', 10
        )

        self.subscription = self.create_subscription(
            ObstacleInfo, '/obstacle', self.obstacle_callback, 10
        )

        self.active_service = self.create_service(
            SetActive, '/set_active', self.set_active_callback
        )

        self.speed_service = self.create_service(
            SetSpeed, '/set_speed', self.set_speed_callback
        )

        self.get_logger().info('Turn Away node started')

    def set_active_callback(self, request, response):
        self.enabled = request.enable

        if not self.enabled:
            self.publisher.publish(Twist())

        response.success = True
        response.message = 'Robot enabled' if self.enabled else 'Robot disabled'
        self.get_logger().info(response.message)
        return response

    def set_speed_callback(self, request, response):
        if request.speed < 0.0:
            response.success = False
            response.message = 'Speed cannot be negative'
        else:
            self.set_parameters([
                rclpy.parameter.Parameter(
                    'forward_speed',
                    rclpy.Parameter.Type.DOUBLE,
                    float(request.speed)
                )
            ])
            response.success = True
            response.message = 'Forward speed updated'

        return response

    def obstacle_callback(self, msg):
        command = Twist()
        status = RobotStatus()

        if not self.enabled:
            status.state = 'disabled'
        else:
            forward_speed = self.get_parameter('forward_speed').value
            turn_speed = self.get_parameter('turn_speed').value
            max_turn_speed = self.get_parameter('max_turn_speed').value

            turn_speed = min(abs(turn_speed), abs(max_turn_speed))

            if not msg.too_close:
                command.linear.x = forward_speed
                status.state = 'moving_forward'
            else:
                command.linear.x = 0.0
                status.state = 'turning'
                command.angular.z = (
                    -turn_speed if msg.angle > 0 else turn_speed
                )

        status.obstacle_distance = msg.distance

        self.publisher.publish(command)
        self.status_publisher.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = TurnAway()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
