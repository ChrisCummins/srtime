from setuptools import setup

setup(name='srtime',
      version='0.0.1',
      description='A statistically rigorous program execution timer',
      url='https://github.com/ChrisCummins/srtime',
      author='Chris Cummins',
      author_email='chrisc.101@gmail.com',
      license='GPL v3',
      packages=['srtime'],
      scripts=['bin/srtime'],
      zip_safe=False)
