#!/usr/bin/env python3

"""
Test script showing how to publish actions and plans
"""

import rclpy
from rclpy.node import Node
import time

from pyrobosim_msgs.msg import TaskAction, TaskPlan


class Commander(Node):
    def __init__(self):
        super().__init__("demo_command_publisher")

        self.declare_parameter("mode", value="plan")

        # Publisher for a single action
        self.action_pub = self.create_publisher(
            TaskAction, "commanded_action", 10)

        # Publisher for a task plan
        self.plan_pub = self.create_publisher(
            TaskPlan, "commanded_plan", 10)

        # Delay to ensure world is loaded.
        time.sleep(2.0)


def main():
    rclpy.init()
    cmd = Commander()

    # Choose between action or plan command, based on input parameter.
    mode = cmd.get_parameter("mode").value
    if mode == "action":
        cmd.get_logger().info("Publishing sample task action...")
        action_msg = TaskAction(type="navigate", target_location="desk")
        cmd.action_pub.publish(action_msg)

    elif mode == "plan":
        cmd.get_logger().info("Publishing sample task plan...")
        task_actions = [
            TaskAction(type="navigate", target_location="desk"),
            TaskAction(type="pick", object="water"),
            TaskAction(type="navigate", target_location="counter"),
            TaskAction(type="place"),
            TaskAction(type="navigate", target_location="kitchen")
        ]
        plan_msg = TaskPlan(actions=task_actions)
        cmd.plan_pub.publish(plan_msg)

    rclpy.spin(cmd)
    cmd.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()