from setuptools import setup, find_packages

setup(
    name='ambientperiod',
    version='0.1.0',
    description='Predominant period estimation from ambient vibration signals',
    author='',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
)
