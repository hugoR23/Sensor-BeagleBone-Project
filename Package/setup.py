from setuptools import setup, find_packages
import sys, os

version = '0.2.1'
shortdesc ='Display data that were retrieved from the BeagleBone through a nice graphical interface.'

install_requires = [
    'setuptools',
    'nose',
    'twisted',
    'matplotlib',
    'webtest',
    'pyramid',
]

entry_points = {
    'console_scripts': [
        'beaglebone = beaglebone.main:main'
    ]
}

setup(name='BeagleBone Project',
      version=version,
      description=shortdesc,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],
      keywords='Sensors, Server-Client communication, Graphics',
      author='Gruppe 3: Quoc-Nam DESSOULES, Louis-Adrien DUFRENE, Claire LOFFLER, Hugo ROBELLAZ, Hang YUAN',
      author_email='qn.dessoulles@telecom-bretagne.eu, la.dufrene@telecom-bretagne.eu, claire.loffler@telecom-sudparis.eu, hugo.robellaz@telecom-bretagne.eu, yuanhangd.c@gmail.com',
      license='AGPLv3+',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points=entry_points
      )


