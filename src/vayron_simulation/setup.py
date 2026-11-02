from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'vayron_simulation'


def collect_directory_tree(source_dir, install_dir):
    data_files = []

    if not os.path.isdir(source_dir):
        return data_files

    for root, _, files in os.walk(source_dir):
        if not files:
            continue

        relative_path = os.path.relpath(root, source_dir)
        destination = (
            install_dir
            if relative_path == '.'
            else os.path.join(install_dir, relative_path)
        )

        source_files = [
            os.path.join(root, filename)
            for filename in files
        ]

        data_files.append((destination, source_files))

    return data_files


data_files = [
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name]
    ),
    (
        'share/' + package_name,
        ['package.xml']
    ),
    (
        os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')
    ),
    (
        os.path.join('share', package_name, 'config'),
        glob('config/*.yaml')
    ),
    (
        os.path.join('share', package_name, 'rviz'),
        glob('rviz/*')
    ),
]

data_files += collect_directory_tree(
    'worlds',
    os.path.join('share', package_name, 'worlds')
)

data_files += collect_directory_tree(
    'models',
    os.path.join('share', package_name, 'models')
)

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jerry',
    maintainer_email='yourrjerry@gmail.com',
    description='Gazebo simulation for VAYRON AMR',
    license='Apache-2.0',
    tests_require=['pytest'],
)
