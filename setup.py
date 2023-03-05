from setuptools import setup

setup(
    name='redis-app',
    version='0.1',
    description='a toy app that uses walrus to interact with redis streams',
    author='Tarek Zaarour',
    author_email='tareqzaarour@gmail.com',
    packages=['app'],
    zip_safe=False
)