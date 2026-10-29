from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'vayron_hardware'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'),
         glob('config/*.yaml')),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Jerry',
    maintainer_email='yourrjerry@gmail.com',
    description='USB serial hardware bridge for VAYRON AMR',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'serial_bridge = vayron_hardware.serial_bridge:main',
        ],
    },
)
