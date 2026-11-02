 # ROS 2 – Introduction to Robotics and Intelligent Systems (Lab 1)

## Course Information

- **Course:** Introduction to Robotics and Intelligent Systems
- **Institution:** Addis Ababa University (AAU)
- **School:** School of Information Technology and Engineering (SiTE)
- **Academic Year:** 2026
- **Lab Assistant:** Mohammed Sraj

## Project Overview

This project implements Lab 1 using **ROS 2 Humble** and **Gazebo Harmonic**. It focuses on developing a differential-drive robot that can use sensors, detect obstacles, communicate through ROS 2 topics and services, and perform movements using actions.

## Implemented Features

### 1. Sensors
- Added a depth camera to the robot.
- Added an IMU sensor.
- Configured ROS 2 topics to publish sensor data.

### 2. Obstacle Detection
- Created an obstacle detector node that subscribes to laser scan data.
- Publishes obstacle information using a custom ROS 2 message.
- Implemented a `turn_away` node that moves forward when the path is clear and turns when an obstacle is detected.

### 3. ROS 2 Parameters
- Added configurable parameters for forward and turning speeds.
- Used parameters to control the robot's movement.

### 4. Custom Messages
- Created a custom `RobotStatus.msg` message.
- Publishes the robot's current state and obstacle distance.

### 5. ROS 2 Services
- Implemented services to activate or deactivate the robot.
- Added a service to change the robot's speed.

### 6. ROS 2 Actions
- Created a `Rotate.action` interface.
- Implemented an action server to rotate the robot by a requested angle.
- Tested the rotation action successfully.

### 7. Action Client – Square Movement
- Created a `square_driver` action client.
- The robot drives four 1-metre sides and performs 90-degree turns.
- Successfully tested the square movement.

## Project Structure

```text
lab1_exercise/
├── diffdrive_bot/
│   ├── config/
│   ├── launch/
│   ├── rviz/
│   ├── scripts/
│   ├── urdf/
│   └── worlds/
│
├── lab_interfaces/
│   ├── action/
│   ├── msg/
│   └── srv/
│
├── my_robot_interfaces/
│
└── my_robot_nodes/
    └── my_robot_nodes/
        ├── turn_away.py
        ├── rotate_action_server.py
        └── square_driver.py
```

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Harmonic
- Python 3

## Build Instructions

Open a terminal inside the ROS 2 environment and run:

```bash
cd ~/ros2_ws
colcon build --packages-up-to my_robot_nodes --symlink-install
```

Source the workspace:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

## Running the Simulation

Launch the Gazebo simulation:

```bash
ros2 launch diffdrive_bot gazebo_headless.launch.py
```

Run the required nodes in separate terminals:

```bash
ros2 run diffdrive_bot obstacle_detector.py
```

```bash
ros2 run diffdrive_bot drive_distance_server.py
```

```bash
ros2 run my_robot_nodes rotate_action_server
```

To test the square movement:

```bash
ros2 run my_robot_nodes square_driver
```

## Testing Results

The following functionalities were tested:

- Gazebo simulation launched successfully.
- Depth camera and IMU topics published sensor data.
- Obstacle detection and custom message publishing were tested.
- ROS 2 parameters and services were tested.
- The rotation action server completed a rotation goal successfully.
- The square movement test completed successfully, with the robot driving four 1-metre sides and making 90-degree turns.

**Note:** Sensor publishing rates may be lower than the configured rates when running the simulation in a Docker/WSL environment.

## Author

**Sosina Zemichael**

Addis Ababa University  
Software Engineering Student
