
from setuptools import find_packages, setup

package_name = 'vayron_teleop'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', []),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jerry',
    maintainer_email='yourrjerry@gmail.com',
    description='Keyboard teleoperation for VAYRON AMR',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'keyboard_teleop = vayron_teleop.keyboard_teleop:main',
        ],
    },
)
