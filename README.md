
<div align="center">

# 🟢 VAYRON-AMR

### AUTONOMOUS MOBILE ROBOTICS PLATFORM

**Engineering Intelligent Mobility Through Robotics, Simulation & Control**

A modular four-wheel differential-drive mobile robot project built with ROS 2, focused on robot modeling, sensor integration, simulation, motor control, and the development of autonomous navigation capabilities.

[![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-39FF14?style=for-the-badge&logo=ros&logoColor=000000)](https://docs.ros.org/en/humble/)
[![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-22.04-39FF14?style=for-the-badge&logo=ubuntu&logoColor=000000)](https://releases.ubuntu.com/22.04/)
[![Gazebo Classic](https://img.shields.io/badge/Simulation-Gazebo_Classic-39FF14?style=for-the-badge)](https://classic.gazebosim.org/)
[![RViz2](https://img.shields.io/badge/Visualization-RViz2-39FF14?style=for-the-badge)](https://github.com/ros2/rviz)

[**Repository**](https://github.com/shivamsb22/VAYRON-AMR) ·
[**Report an Issue**](https://github.com/shivamsb22/VAYRON-AMR/issues) ·
[**ROS 2 Documentation**](https://docs.ros.org/en/humble/)

<br>

**PROJECT STATUS: ACTIVE DEVELOPMENT**

</div>

---

## 01 — Overview

VAYRON-AMR is a mobile robotics platform being developed to explore the integration of mechanical design, embedded motor control, robot simulation, perception, and autonomous navigation.

The platform uses a **four-wheel differential-drive configuration**. The left-side wheels operate as one drive group and the right-side wheels as the other. By controlling the relative speeds and directions of these groups, the robot can move forward, reverse, turn, and rotate in place, subject to its mechanical design and traction.

The project combines two development areas:

- **Embedded robotics:** Arduino-based motor control and a four-channel motor driver.
- **ROS 2 robotics:** Robot description, simulation, coordinate frames, sensor visualization, and the development of control and navigation software.

The objective is to build and validate the software architecture in simulation before integrating and testing the corresponding physical hardware.

## 02 — Project Objectives

- Develop a modular robot description using URDF and Xacro.
- Model the four-wheel differential-drive platform.
- Simulate the robot in Gazebo Classic.
- Visualize the robot model, transforms, and sensor data in RViz2.
- Establish a reliable interface between high-level robot commands and embedded motor control.
- Integrate LiDAR-based perception and mapping.
- Develop localization and autonomous navigation capabilities.
- Maintain a modular, documented, and reproducible ROS 2 workspace.

## 03 — Robot Specifications

| Parameter | Description |
|---|---|
| Robot name | VAYRON-AMR |
| Robot category | Autonomous Mobile Robot (AMR) |
| Drive configuration | Four-wheel differential drive |
| Drive grouping | Left and right wheel pairs |
| Embedded controller | Arduino; exact board model to be documented |
| Motor driver | Four-channel motor driver; exact model to be documented |
| Robotics middleware | ROS 2 Humble |
| Operating system | Ubuntu 22.04 LTS |
| Robot description | URDF / Xacro |
| Simulation | Gazebo Classic |
| Visualization | RViz2 |
| Simulated LiDAR | Gazebo ray sensor integration |
| Navigation framework | Nav2 planned for integration |
| Mapping | SLAM integration planned / under development |

> **Specification note:** Hardware model numbers, motor ratings, dimensions, battery specifications, and measured performance will be documented after they are verified. The presence of a package or configuration file does not mean that its complete functionality has been implemented or tested.

## 04 — Hardware Components

The table below documents the known hardware architecture. Exact product models and electrical specifications should be added after confirming the parts used in the physical robot.

| Component | Quantity | Purpose | Why it is used |
|---|---:|---|---|
| Arduino development board | 1 | Embedded motor-control logic | Receives control instructions and generates the signals needed to operate the motor driver. |
| Four-channel motor driver | 1 | Motor power switching and direction control | Provides the motor-control channels required by the four-wheel arrangement, subject to the driver's supported wiring and current ratings. |
| DC geared motors | 4 | Wheel propulsion | Convert electrical energy into rotational motion and provide torque for moving the robot. |
| Robot wheels | 4 | Ground contact and locomotion | Provide traction and transfer motor torque to the ground. |
| Robot chassis | 1 assembly | Mechanical structure | Supports the motors, wheels, controller, power system, and other components. |
| Motor power source | To be confirmed | Supplies the drive system | Must meet the motor voltage and current requirements, including startup and stall current. |
| Wiring and connectors | As required | Electrical interconnection | Connect the controller, motor driver, motors, and power distribution safely. |
| LiDAR sensor | Physical model to be confirmed | Distance sensing and mapping | Intended to provide range measurements for perception and mapping. A simulated LiDAR is configured in the current Gazebo description. |

### How the Drive System Works

The four wheels are controlled as two drive groups:

- **Forward motion:** Both sides rotate in the direction required for forward travel.
- **Reverse motion:** Both sides reverse direction.
- **Left turn:** The right side moves faster than the left side, or the sides rotate in opposite directions for a tighter turn.
- **Right turn:** The left side moves faster than the right side, or the sides rotate in opposite directions for a tighter turn.
- **Rotation in place:** The two sides rotate in opposite directions, provided the motor control and mechanical arrangement support it.

This is a differential-drive arrangement, not a mecanum-drive arrangement. Lateral movement without turning is not a native capability of this configuration.

### Electrical Integration Considerations

- Confirm the motor driver's rated voltage and continuous and peak current before connecting motors.
- Use a suitable power supply for the motors and a correctly regulated supply for the Arduino.
- Establish a common signal ground when required by the selected driver and controller interface.
- Do not power motors directly from Arduino GPIO pins.
- Verify polarity, wiring, fusing, and emergency-stop arrangements before physical testing.

## 05 — Software Stack

| Technology | Role in VAYRON-AMR | Why it is used |
|---|---|---|
| Ubuntu 22.04 LTS | Operating system | Provides the target environment for ROS 2 Humble. |
| ROS 2 Humble | Robotics middleware | Connects robot software through nodes, topics, services, and actions. |
| URDF | Robot model description | Defines links, joints, and the robot's kinematic structure. |
| Xacro | Robot description authoring | Allows reusable macros and parameters to organize the robot model. |
| Gazebo Classic | Physics-based simulation | Enables development and testing without requiring the physical robot for every iteration. |
| RViz2 | Robot visualization | Displays the robot model, TF frames, and supported sensor data. |
| `robot_state_publisher` | Transform publication | Publishes robot link transforms from the URDF and joint states. |
| `joint_state_publisher` | Joint-state support | Publishes configured joint states where appropriate for the model and workflow. |
| `ros_gz` / Gazebo ROS integration | Simulation-to-ROS communication | Connects supported simulated sensors and robot systems to ROS topics. This project currently uses Gazebo Classic integration packages. |
| Arduino firmware | Embedded motor control | Handles low-level motor commands and the hardware-specific interface. |
| Nav2 | Navigation framework | Intended to provide path planning, navigation behaviors, and navigation orchestration. |
| SLAM Toolbox | Mapping | Intended to build a map from supported laser scan and odometry inputs. |

**Compatibility note:** This workspace uses Gazebo Classic integration. Modern Gazebo and Gazebo Classic have different integration stacks, so packages and plugins must match the installed simulator version.

## 06 — System Architecture

The intended system is divided into hardware control, robot modeling, perception, and navigation layers.

```text
                 HIGH-LEVEL ROBOT SOFTWARE
              ROS 2 Humble / Navigation Layer
                           |
                           v
                    /cmd_vel commands
                           |
                           v
               Embedded Control Interface
                ROS 2 Node / Serial Link
                           |
                           v
                      Arduino
                           |
                           v
                 Four-Channel Motor Driver
                           |
              +------------+------------+
              |            |            |
           Left pair   Right pair   Motor power
              |            |
              +-----+------+
                    |
                    v
             Four-Wheel AMR
```

The perception and simulation path is intended to follow this structure:

```text
URDF / Xacro
     |
     v
Robot State Publisher -----> TF transforms
     |
     +-----> RViz2
     |
     +-----> Gazebo Classic
                  |
                  v
           Simulated LiDAR
                  |
                  v
                /scan
                  |
                  v
        Mapping / Localization
                  |
                  v
              Nav2 (planned)
```

> These diagrams describe the intended architecture. Hardware communication, closed-loop wheel control, odometry, SLAM, and Nav2 must each be verified independently before they are represented as operational features.

## 07 — Repository Structure

```text
VAYRON-AMR/
├── .gitignore
├── README.md
├── docs/
│   └── images/
└── src/
    ├── vayron_description/
    │   ├── launch/
    │   │   └── vayron.launch.py
    │   ├── rviz/
    │   │   └── vayron.rviz
    │   └── urdf/
    │       └── vayron/
    │           ├── vayron.urdf
    │           └── vayron.urdf.xacro
    │
    ├── vayron_bringup/
    ├── vayron_control/
    ├── vayron_hardware/
    ├── vayron_navigation/
    └── vayron_simulation/
```

### Package Responsibilities

| Package | Responsibility |
|---|---|
| `vayron_description` | Robot links, joints, Xacro/URDF files, visualization configuration, and description launch files. |
| `vayron_bringup` | Intended entry point for starting the complete robot system. |
| `vayron_control` | Intended location for motion-control nodes and drive-control logic. |
| `vayron_hardware` | Intended location for Arduino communication and hardware interfaces. |
| `vayron_navigation` | Intended location for mapping, localization, navigation parameters, and related launch files. |
| `vayron_simulation` | Intended location for simulation-specific assets and launch configuration. |

Some packages currently contain ROS 2 package scaffolding only. Their responsibilities describe the planned modular design, not necessarily completed functionality.

## 08 — Installation

### Prerequisites

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Gazebo Classic and compatible ROS integration packages
- Git
- `colcon`
- `rosdep`

Install the build tools if they are not already available:

```bash
sudo apt update
sudo apt install -y \
  git \
  python3-colcon-common-extensions \
  python3-rosdep
```

Install the ROS 2 Humble Gazebo Classic integration package if it is available for your configured ROS installation:

```bash
sudo apt install ros-humble-gazebo-ros
```

### Clone the Repository

```bash
git clone https://github.com/shivamsb22/VAYRON-AMR.git
cd VAYRON-AMR
```

### Resolve Dependencies

```bash
source /opt/ros/humble/setup.bash

rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

If `rosdep` reports missing dependency declarations, resolve those before proceeding.

### Build the Workspace

```bash
cd ~/VAYRON-AMR

source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

> If your local workspace is named `vayron_ws`, use `cd ~/vayron_ws` instead. The GitHub repository name and local directory name do not have to match.

## 09 — Launching the Robot Description

The current description launch file is:

`vayron_description/launch/vayron.launch.py`

Launch the robot using:

```bash
source /opt/ros/humble/setup.bash
source ~/vayron_ws/install/setup.bash

ros2 launch vayron_description vayron.launch.py
```

The launch configuration is intended to start the robot description and visualization/simulation components configured in the package.

Exact launch behavior depends on the current launch file, installed plugins, and local environment.

### Verify ROS 2 Topics

In another terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/vayron_ws/install/setup.bash

ros2 topic list
```

Check the simulated laser scan topic:

```bash
ros2 topic echo /scan
```

Check available transforms:

```bash
ros2 run tf2_tools view_frames
```

These commands help verify whether the corresponding topics and transforms are actually being published.

## 10 — Development Roadmap

### Robot Modeling and Simulation

- [x] ROS 2 workspace initialized
- [x] Modular package structure created
- [x] Initial URDF/Xacro robot model created
- [x] Gazebo/RViz launch integration created
- [x] Simulated LiDAR integration configured
- [ ] Validate all link and joint transforms
- [ ] Validate the robot model and sensor positions in simulation

### Motion Control

- [ ] Implement and verify the differential-drive controller
- [ ] Establish the ROS 2 to Arduino communication protocol
- [ ] Implement motor direction and speed control
- [ ] Validate safe stopping and command timeouts
- [ ] Integrate wheel encoders and odometry if supported by the hardware
- [ ] Verify keyboard teleoperation in simulation

### Perception and Navigation

- [ ] Validate `/scan` data and sensor frame alignment
- [ ] Integrate and validate SLAM Toolbox
- [ ] Configure localization and map loading
- [ ] Integrate Nav2
- [ ] Test goal navigation and obstacle avoidance
- [ ] Validate the complete workflow on physical hardware

## 11 — Troubleshooting

| Problem | Checks |
|---|---|
| Package not found | Source `/opt/ros/humble/setup.bash`, rebuild with `colcon build`, and source the workspace's `install/setup.bash`. |
| Robot model not visible | Check the URDF/Xacro, robot description topic, Fixed Frame, and TF tree. |
| LiDAR data missing | Check the Gazebo sensor plugin, sensor topic, frame ID, and `ros2 topic echo /scan`. |
| Gazebo plugin fails to load | Confirm the plugin library is installed and compatible with Gazebo Classic. |
| Robot does not move | Verify the drive plugin or controller, `/cmd_vel` subscriber, motor-control implementation, and hardware communication. |
| RViz displays transform errors | Confirm the Fixed Frame exists and the required TF transforms are being published. |
| Build fails | Read the first actual compiler or dependency error, fix it, and rebuild the affected package. |

## 12 — Engineering Principles

VAYRON-AMR follows a modular development approach:

- **Simulation first:** validate software behavior before physical integration.
- **Modularity:** keep robot description, control, hardware, and navigation concerns separate.
- **Verifiability:** distinguish implemented features from planned features.
- **Safety:** validate electrical ratings, motor behavior, and stopping mechanisms before operation.
- **Documentation:** keep setup steps, component specifications, and testing results reproducible.

## 13 — Screenshots and Demonstrations

Robot screenshots, Gazebo views, RViz visualizations, architecture diagrams, and demonstration videos will be added as they become available.

Suggested documentation assets:

```text
docs/
└── images/
    ├── vayron-overview.png
    ├── gazebo-simulation.png
    ├── rviz-visualization.png
    └── system-architecture.png
```

These are suggested filenames only. Add each image before referencing it in the README.

## 14 — Contributing

Contributions and technical feedback are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Build and test the affected packages.
5. Document the implementation and verification steps.
6. Submit a pull request with a clear description.

## 15 — License

A license has not yet been selected. Until a license is added, permission to reuse, modify, or redistribute this project should not be assumed.

---

<div align="center">

### VAYRON-AMR

**DESIGN. BUILD. SIMULATE. VALIDATE.**

*Engineering autonomy, one subsystem at a time.*

[Repository](https://github.com/shivamsb22/VAYRON-AMR) · [Issues](https://github.com/shivamsb22/VAYRON-AMR/issues)

</div>
