<div align="center">

<img src="docs/images/vayron-header-banner.png" alt="VAYRON-AMR | Autonomous Mobile Robotics Platform" width="100%">

<br>

# VAYRON-AMR

### Autonomous Mobile Robotics Platform

**Design · Control · Simulation · Navigation**

<br>

[![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![Gazebo Classic](https://img.shields.io/badge/Gazebo-Classic-1677FF?style=for-the-badge)](https://classic.gazebosim.org/)
[![RViz2](https://img.shields.io/badge/Visualization-RViz2-00BFEA?style=for-the-badge)](https://docs.ros.org/en/humble/)

<br>

*A ROS 2-based mobile robotics project focused on robot description, simulation, control, and a foundation for autonomous navigation.*

</div>

---

## Contents

- [Overview](#-overview)
- [Project Goals](#-project-goals)
- [Robot Platform](#-robot-platform)
- [Technology Stack](#-technology-stack)
- [Repository Structure](#-repository-structure)
- [System Architecture](#-system-architecture)
- [Getting Started](#-getting-started)
- [Build the Workspace](#-build-the-workspace)
- [Launch and Visualize](#-launch-and-visualize)
- [Development Status](#-development-status)
- [Troubleshooting](#-troubleshooting)
- [Engineering Notes](#-engineering-notes)
- [Author](#-author)

---

## 🤖 Overview

**VAYRON-AMR** is a robotics development project built around ROS 2 Humble. The repository organizes the robot description and the planned software layers for bringup, control, hardware communication, navigation, and simulation.

The goal is to build a maintainable base for an Autonomous Mobile Robot (AMR), with a workflow that can progress from a robot model and visualization to simulated testing and, later, hardware integration and autonomous navigation.

> **Project status:** This repository is under active development. Features listed as planned or in progress should not be interpreted as fully implemented or hardware-validated.

## 🎯 Project Goals

- Maintain a modular ROS 2 workspace with clearly separated packages.
- Describe the VAYRON robot using URDF/Xacro.
- Visualize the robot and its frames in RViz2.
- Develop and test the robot model in Gazebo Classic.
- Build a control layer for the four-wheel drive configuration.
- Prepare interfaces for future Arduino-based hardware communication.
- Develop toward SLAM and Nav2-based autonomous navigation.
- Keep setup, launch, and development instructions reproducible.

## 🛞 Robot Platform

| Property | Current project direction |
|---|---|
| Platform | VAYRON-AMR |
| Robot type | Autonomous Mobile Robot (AMR) |
| Drive configuration | Four-wheel differential drive, with left and right wheels controlled as sides |
| Robotics middleware | ROS 2 Humble |
| Robot description | URDF / Xacro |
| Visualization | RViz2 |
| Simulation | Gazebo Classic |
| Hardware integration direction | Arduino and a four-channel motor driver |
| Navigation direction | SLAM Toolbox and Nav2, as implementation progresses |

**Note:** Exact Arduino and motor-driver models, final sensor specifications, and verified physical performance figures are not stated here because they have not been confirmed in the project details.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| ROS 2 Humble | Nodes, topics, launch system, and package integration |
| URDF / Xacro | Robot geometry, links, joints, and reusable robot description |
| RViz2 | Robot model and TF visualization |
| Gazebo Classic | Robot simulation and environment testing |
| `colcon` | Workspace build tool |
| Arduino | Intended low-level hardware interface |
| SLAM Toolbox | Planned mapping workflow |
| Nav2 | Planned autonomous navigation stack |
| Git / GitHub | Version control and project documentation |

## 📁 Repository Structure

```text
vayron_ws/
├── src/
│   ├── vayron_description/
│   │   ├── launch/
│   │   │   └── vayron.launch.py
│   │   ├── rviz/
│   │   │   └── vayron.rviz
│   │   └── urdf/
│   │       └── vayron/
│   │           ├── vayron.urdf
│   │           └── vayron.urdf.xacro
│   ├── vayron_bringup/
│   ├── vayron_control/
│   ├── vayron_hardware/
│   ├── vayron_navigation/
│   └── vayron_simulation/
├── docs/
│   └── images/
│       └── vayron-banner.png
├── .gitignore
└── README.md
```

Some packages may currently contain only their initial structure. The tree above describes the workspace organization, not a guarantee that every layer is complete.

## 🧩 System Architecture

The intended high-level data flow is:

```text
                 ┌─────────────────────────┐
                 │   Robot Description     │
                 │      URDF / Xacro       │
                 └────────────┬────────────┘
                              │
                 ┌────────────▼────────────┐
                 │   Bringup / Launch      │
                 └────────────┬────────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
     ┌────────▼───────┐ ┌─────▼──────┐ ┌───────▼────────┐
     │ RViz2 / TF     │ │ Simulation │ │ Control Layer  │
     │ Visualization  │ │ Gazebo     │ │ ROS 2          │
     └────────────────┘ └────────────┘ └───────┬────────┘
                                               │
                                      ┌────────▼────────┐
                                      │ Hardware Bridge │
                                      │ Arduino (planned)│
                                      └─────────────────┘
```

The diagram represents the intended architecture. Hardware communication and the complete navigation pipeline require implementation and validation before they can be described as operational.

## 🚀 Getting Started

### Prerequisites

The project is intended for:

- Ubuntu 22.04 LTS
- ROS 2 Humble
- `colcon`
- RViz2
- Gazebo Classic and the ROS integration packages, if running the simulation

Install the general build tools:

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions python3-rosdep git
```

If ROS 2 Humble is already installed, source its environment:

```bash
source /opt/ros/humble/setup.bash
```

If ROS 2 is not installed, follow the official [ROS 2 Humble installation guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html). For Gazebo Classic integration, check package availability for your ROS installation and follow the relevant [ROS 2 Gazebo documentation](https://classic.gazebosim.org/tutorials?tut=ros2_overview).

### Clone the repository

```bash
git clone https://github.com/shivamsb22/VAYRON-AMR.git
cd VAYRON-AMR
```

If your local workspace folder is named `vayron_ws`, enter that folder instead. Keep the repository root and the ROS workspace root consistent with your actual directory layout.

## 🏗️ Build the Workspace

From the directory that contains `src/`:

```bash
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

For future terminals, source both environments:

```bash
source /opt/ros/humble/setup.bash
source ~/vayron_ws/install/setup.bash
```

If the repository itself is at `~/VAYRON-AMR` rather than `~/vayron_ws`, update the second path accordingly.

## 🖥️ Launch and Visualize

The repository includes a launch file at:

```text
src/vayron_description/launch/vayron.launch.py
```

Once the workspace builds successfully, try:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch vayron_description vayron.launch.py
```

This command assumes the package metadata and launch file are installed correctly and that the launch file is registered by the package. If the package does not expose this launch file yet, inspect its `package.xml`, `setup.py` or `CMakeLists.txt`, then adjust the launch installation rules.

To open RViz2 separately:

```bash
rviz2
```

If the project has a saved RViz configuration and it is installed or available by path, load it with:

```bash
rviz2 -d src/vayron_description/rviz/vayron.rviz
```

Simulation launch commands depend on the current implementation of `vayron_simulation`. Do not assume a simulation launch target exists until it is added and tested.

## 🧪 Development Status

| Component | Status |
|---|---|
| Workspace and package organization | Established |
| URDF / Xacro robot description | Present; continue validating geometry and joint configuration |
| RViz2 configuration | Present |
| Description launch file | Present; verify package installation and launch behavior |
| Gazebo simulation | Under development; verify current launch and plugin configuration |
| ROS 2 drive control | Under development |
| Arduino hardware bridge | Planned / requires hardware validation |
| SLAM mapping | Planned / requires end-to-end testing |
| Nav2 autonomous navigation | Planned / requires end-to-end testing |
| Documentation and visuals | In progress |

Update this table as features become testable. A README is project documentation, not a wish-granting device.

## 🔧 Troubleshooting

### ROS 2 commands are not found

```bash
source /opt/ros/humble/setup.bash
```

### Packages are not discovered

Run these commands from the workspace root:

```bash
colcon list
colcon build --symlink-install
source install/setup.bash
```

### A launch file cannot be found

Check that the package exists and the launch file is installed:

```bash
ros2 pkg list | grep vayron
find src/vayron_description/launch -maxdepth 1 -type f
```

For Python packages, check the `setup.py` data files. For CMake packages, check the launch-directory install rules in `CMakeLists.txt`.

### RViz2 does not display the robot

Check that the robot description is being published, the fixed frame exists, and the required TF transforms are available:

```bash
ros2 topic list
ros2 topic echo /robot_description
ros2 run tf2_tools view_frames
```

The exact topics and available tools can vary with the launch configuration. If `/robot_description` is not a topic in your setup, inspect the active nodes and parameters instead of assuming every ROS installation behaves identically.

## 🧠 Engineering Notes

- Keep simulated behavior separate from hardware claims.
- Prefer small, reviewable commits and descriptive commit messages.
- Validate URDF links, joints, wheel axes, and TF frames before tuning controllers.
- Document tested commands and software versions when behavior changes.
- Do not commit build output, generated logs, credentials, tokens, or local environment files.
- Record sensor models, motor specifications, and measured performance only after confirming them.

## 👨‍💻 Author

<div align="center">

### Project developed by

# 𝓙𝓮𝓻𝓻𝔂

**Robotics & Automation Engineer**

*Building mobile robots, one verified subsystem at a time.*

<br>

<a href="https://github.com/shivamsb22">
  <img src="https://img.shields.io/badge/GitHub-My%20Profile-00D9FF?style=for-the-badge&logo=github&logoColor=111827" alt="Jerry's GitHub Profile">
</a>

<a href="YOUR_LINKEDIN_PROFILE_URL">
  <img src="https://img.shields.io/badge/LinkedIn-My%20Profile-1677FF?style=for-the-badge&logo=linkedin&logoColor=white" alt="Jerry's LinkedIn Profile">
</a>

<br>

<sub>VAYRON-AMR · Autonomous Mobile Robotics</sub>

</div>

---

<div align="center">
<sub>Built with ROS 2 · Documented on GitHub · Continuously evolving</sub>
</div>
