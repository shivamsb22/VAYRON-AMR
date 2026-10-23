cmake_minimum_required(VERSION 3.8)
project(vayron_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf launch rviz meshes worlds models
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
)

ament_package()
