from setuptools import setup

package_name = 'angel_ss'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='song',
    maintainer_email='sms0432@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'angel_ss_temp = angel_ss.angel_ss_temp:main',
            'angel_ss_version = angel_ss.angel_ss_version:main'
        ],
    },
)
