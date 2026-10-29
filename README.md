<div align="center">

<img src="docs/images/vayron-header-banner.png" alt="VAYRON-AMR banner" width="100%">

# VAYRON-AMR

### Autonomous Mobile Robotics Platform

**Design · Simulate · Integrate · Navigate**

A modular four-wheel differential-drive Autonomous Mobile Robot (AMR) project built with ROS 2 Humble. The repository organizes robot description, simulation, control, hardware integration, mapping, and navigation into separate packages for modular development and testing.

[![ROS 2](https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros)](https://docs.ros.org/en/humble/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![Platform](https://img.shields.io/badge/Platform-AMR-0A7B83)](#project-overview)
[![Status](https://img.shields.io/badge/Status-Development-orange)](#project-status)

</div>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Goals](#project-goals)
- [Project Status](#project-status)
- [Robot Configuration](#robot-configuration)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Build the Workspace](#build-the-workspace)
- [Simulation](#simulation)
- [Teleoperation and ROS 2 Checks](#teleoperation-and-ros-2-checks)
- [Mapping and Navigation](#mapping-and-navigation)
- [Troubleshooting](#troubleshooting)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Project Signature](#project-signature)

---

## Project Overview

**VAYRON-AMR** is a robotics development project focused on building a compact, budget-conscious Autonomous Mobile Robot.

The project follows a modular ROS 2 architecture, separating the robot model, simulation, control, hardware interfaces, and navigation software.

The intended development workflow is:

1. Design and validate the robot model.
2. Simulate the robot in Gazebo Classic.
3. Verify motion commands and safe-stop behavior.
4. Integrate the physical controller and sensors.
5. Implement and validate mapping and localization.
6. Test autonomous navigation after validating the required subsystems.

> **Development note:** The presence of a package or configuration file does not mean that the corresponding feature has been fully implemented or tested. Features should be marked complete only after successful validation.

## Project Goals

- Develop a compact four-wheel skid-steer mobile robot.
- Use ROS 2 Humble as the robotics middleware.
- Keep description, simulation, control, hardware, and navigation modular.
- Validate software behavior in simulation before physical integration.
- Work toward LiDAR-based mapping and autonomous navigation.
- Maintain reproducible setup instructions and clear technical documentation.

## Project Status

The repository contains the initial workspace structure, robot description files, simulation launch files and worlds, RViz configuration, navigation configuration, a sample map, and a velocity watchdog script.

| Subsystem | Repository contents | Next validation step |
|---|---|---|
| Robot description | URDF/Xacro model | Validate links, joints, and TF |
| Simulation | Gazebo launch files and worlds | Test launch and robot spawning |
| Visualization | RViz configuration | Verify displays and fixed frame |
| Velocity watchdog | `cmd_vel_watchdog.py` | Test timeout and stop behavior |
| Control | ROS 2 package | Implement and test control logic |
| Hardware | ROS 2 package | Validate controller communication |
| Mapping | SLAM configuration and launch file | Verify LiDAR and mapping |
| Navigation | Nav2 configuration and sample map | Validate localization and navigation |

Update this table as individual subsystems are tested. Do not claim successful operation without test results.

## Robot Configuration

VAYRON is designed around a four-wheel skid-steer drive configuration.

The left-side wheels work together, and the right-side wheels work together to control forward movement, reverse movement, and turning.

| Component | Intended purpose |
|---|---|
| Four geared DC motors | Drive the robot |
| Motor drivers | Control motor direction and speed |
| Arduino controller | Handle low-level motor control |
| Raspberry Pi or Linux computer | Run ROS 2 and higher-level robotics software |
| 2D LiDAR | Provide range measurements for mapping |
| Wheel encoders | Provide wheel-motion feedback, if supported |
| Robot chassis | Support the electronics and drive system |
| Optional camera and sensors | Extend perception capabilities |

Select the final components according to the actual hardware build. Verify voltage, current, wiring, grounding, and driver ratings before connecting the electronics.

## Technology Stack

| Technology | Purpose |
|---|---|
| Ubuntu 22.04 | Operating system |
| ROS 2 Humble | Robotics middleware |
| URDF / Xacro | Robot modeling |
| Gazebo Classic | Robot simulation |
| RViz | Robot visualization |
| SLAM Toolbox | Mapping |
| Nav2 | Autonomous navigation |
| Arduino | Intended low-level motor control |
| Git / GitHub | Version control |

## Repository Structure

The workspace follows this general structure:

```text
vayron_ws/
├── docs/
│   ├── architecture/
│   └── images/
│       └── vayron-header-banner.png
├── maps/
│   ├── sample.pgm
│   └── sample.yaml
├── src/
│   ├── vayron_bringup/
│   ├── vayron_control/
│   ├── vayron_description/
│   │   ├── launch/
│   │   ├── rviz/
│   │   ├── scripts/
│   │   └── urdf/
│   ├── vayron_hardware/
│   ├── vayron_navigation/
│   │   ├── config/
│   │   └── launch/
│   └── vayron_simulation/
│       ├── launch/
│       └── worlds/
└── README.md
```

### Package responsibilities

| Package | Responsibility |
|---|---|
| `vayron_description` | Robot model, state publishing, RViz configuration, and description utilities |
| `vayron_simulation` | Gazebo worlds and simulation launch files |
| `vayron_control` | Motion-control logic and controller integration |
| `vayron_hardware` | Physical controller and hardware interfaces |
| `vayron_navigation` | SLAM and Nav2 configurations and launch files |
| `vayron_bringup` | Coordinated startup of robot subsystems |

These are intended responsibilities. Check the actual implementation of each package before relying on a feature.

## System Architecture

The intended data flow is illustrated below:

```text
             Operator / Navigation Goal
                        |
                        v
               ROS 2 Navigation
                  SLAM / Nav2
                        |
                        v
                     /cmd_vel
                        |
                        v
               Velocity Watchdog
                        |
                        v
                Control Interface
                        |
                        v
                Arduino Controller
                        |
                        v
               Motor Drivers / Motors


LiDAR ----------------> Sensor Topics
Wheel Encoders -------> Odometry Feedback
Robot Description ----> TF / Robot State
```

The diagram represents the intended architecture, not proof that every connection is currently implemented. Confirm the actual topic names, transforms, and hardware interfaces during testing.

## Prerequisites

Before building the workspace, install or verify:

- Ubuntu 22.04
- ROS 2 Humble
- `colcon`
- `rosdep`
- Git
- Gazebo Classic and the required ROS integration packages
- RViz and the required navigation packages

Check the ROS installation:

```bash
printenv ROS_DISTRO
which ros2
```

The expected ROS distribution is `humble`.

## Installation

### 1. Clone the repository

If you have not cloned the repository yet:

```bash
mkdir -p ~/vayron_ws/src
cd ~/vayron_ws/src

git clone https://github.com/shivamsb22/VAYRON-AMR.git
```

If you already have the repository in `~/vayron_ws`, do not clone it again inside the existing workspace.

### 2. Source ROS 2

```bash
source /opt/ros/humble/setup.bash
```

### 3. Install dependencies

Run from the workspace root:

```bash
cd ~/vayron_ws

rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

Resolve any missing dependency keys rather than silently skipping errors.

## Build the Workspace

Build the packages:

```bash
cd ~/vayron_ws

source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

After a successful build, source the workspace:

```bash
source ~/vayron_ws/install/setup.bash
```

For every new terminal, source both environments:

```bash
source /opt/ros/humble/setup.bash
source ~/vayron_ws/install/setup.bash
```

Check package discovery:

```bash
ros2 pkg list | grep '^vayron_'
```

If a package fails to build, resolve the first relevant error in the output before proceeding.

## Simulation

The repository contains launch files for an indoor test facility and a city environment.

Run the commands from the workspace root after sourcing ROS 2 and the workspace overlay.

### Indoor test facility

```bash
cd ~/vayron_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch vayron_simulation vayron_indoor.launch.py
```

### City environment

```bash
cd ~/vayron_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch vayron_simulation city.launch.py
```

These commands assume the packages have been built successfully and the launch files are installed correctly.

### Verify the simulation

In a separate terminal, source the environment and inspect the active ROS graph:

```bash
source /opt/ros/humble/setup.bash
source ~/vayron_ws/install/setup.bash

ros2 node list
ros2 topic list
```

Check the command topic:

```bash
ros2 topic info /cmd_vel
```

The topic may not show messages until a command publisher is active. Verify robot spawning, Gazebo logs, and node status if the simulation does not start as expected.

## Teleoperation and ROS 2 Checks

If `teleop_twist_keyboard` is installed, launch keyboard teleoperation:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Confirm that the published command topic matches the topic consumed by the robot control system.

Inspect the command topic:

```bash
ros2 topic info /cmd_vel
ros2 topic echo /cmd_vel
```

Inspect available transforms and joint states:

```bash
ros2 topic list
ros2 topic echo /tf
ros2 topic echo /joint_states
```

A topic may be unavailable until its corresponding node or plugin is running. Use the active topic list to confirm names.

### Velocity watchdog

The repository includes a command-velocity watchdog intended to stop stale velocity commands.

Test the watchdog in simulation before connecting it to physical motors.

Verify that:

1. Fresh commands are handled as expected.
2. Velocity commands stop after the configured timeout.
3. Stopping the command publisher does not leave the robot moving.
4. The watchdog input and output topics match the control system.

A software watchdog is not a substitute for a physical emergency-stop mechanism.

## Mapping and Navigation

Mapping and autonomous navigation require valid sensor data, transforms, odometry, and robot configuration. Validate these dependencies before attempting navigation.

### SLAM Toolbox

The repository contains a SLAM Toolbox configuration and launch file.

Inspect the launch file and confirm its expected topic names and frame parameters. Then run:

```bash
ros2 launch vayron_navigation slam.launch.py
```

Verify that the LiDAR topic is publishing:

```bash
ros2 topic list
ros2 topic info /scan
ros2 topic echo /scan
```

These commands assume the LiDAR topic is `/scan`. If the sensor uses another topic, update the configuration or remap the topic appropriately.

Confirm that the LiDAR frame exists in TF and that the robot moves consistently with the mapping data.

### Sample map

The repository contains:

```text
maps/sample.yaml
maps/sample.pgm
```

Check that the YAML file references the correct image path and that the map resolution and origin are appropriate for the map.

### Nav2 configuration

The navigation configuration is located at:

```text
src/vayron_navigation/config/nav2_params.yaml
```

After verifying the robot model, odometry, TF, sensor data, and localization configuration, Nav2 can be tested with the sample map.

Run from the workspace root:

```bash
cd ~/vayron_ws

ros2 launch nav2_bringup bringup_launch.py \
  map:="$(pwd)/maps/sample.yaml" \
  use_sim_time:=True \
  params_file:="$(pwd)/src/vayron_navigation/config/nav2_params.yaml" \
  autostart:=True
```

This is a starting command, not a guarantee that the current configuration is ready for autonomous navigation.

Before sending a navigation goal, verify:

- Map loading and localization
- Correct TF frames
- Valid odometry
- Sensor data and obstacle observations
- Costmap configuration
- Planner and controller configuration
- Lifecycle nodes and action servers

Do not run autonomous navigation until the required nodes and topics are working correctly.

## Troubleshooting

| Problem | What to check |
|---|---|
| `ros2` command not found | Source ROS 2 Humble and verify the installation |
| Package or launch file not found | Rebuild the workspace and source `install/setup.bash` |
| Robot does not appear in Gazebo | Check robot description, spawn service, launch logs, and model validity |
| Robot does not move | Check `/cmd_vel`, topic remappings, controller configuration, and motor interfaces |
| LiDAR data is missing | Check sensor startup, topic name, message type, and frame ID |
| Robot model is missing in RViz | Check `robot_description`, TF, fixed frame, and display settings |
| Map is not visible in RViz | Check the map topic, fixed frame, and map display configuration |
| Nav2 fails to start | Check parameters, map path, lifecycle nodes, TF, odometry, and localization |
| Physical hardware does not respond | Check voltage, wiring, common ground, driver ratings, firmware, and stop behavior |

Investigate the first meaningful error in the terminal logs. Later errors may be consequences of the original failure.

## Development Roadmap

- [ ] Validate the URDF/Xacro model and TF tree.
- [ ] Verify both Gazebo worlds and robot spawning.
- [ ] Test keyboard teleoperation in simulation.
- [ ] Validate watchdog timeout and stop behavior.
- [ ] Implement the Arduino motor-control interface.
- [ ] Integrate wheel encoders and validate odometry.
- [ ] Integrate LiDAR and verify sensor frames.
- [ ] Generate and save a map using SLAM Toolbox.
- [ ] Configure localization and validate Nav2 in simulation.
- [ ] Integrate physical hardware incrementally.
- [ ] Document verified test results, wiring, and calibration.

## Contributing

Technical feedback and contributions are welcome.

1. Fork the repository.
2. Create a focused feature branch.
3. Make and document your changes.
4. Build and test the affected packages.
5. Open a pull request with a clear summary and test results.

Keep changes modular and document any limitations or untested behavior.

## License

Refer to the repository's `LICENSE` file for the applicable license and reuse terms.

If no license file exists, specify the intended license before distributing the project for reuse.

---

## Project Signature

<div align="center">

**Designed and developed by**

### <em>𝒥𝑒𝓇𝓇𝓎</em>

*VAYRON-AMR · Autonomous Robotics Project*

</div>
