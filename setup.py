from setuptools import setup, Extension

module = Extension('example', sources = ['RPi5-Loki-Files/example.pyx'])

setup(
    name='IoT-Security-Project',
    version='0.3',
    packages=[''],
    url='',
    license='MIT License ',
    author='patap',
    author_email='',
    description='',
    ext_modules = [module]
)
