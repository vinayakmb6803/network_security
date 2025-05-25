'''
The setup.py file is an essential part of packaging and distributing python projects.
it is used by setuptools (or distutils) to define the configuration of your project, such as its metadata, dependencies, and entry points.
This file is used to create a package that can be installed using pip.
'''
from setuptools import find_packages, setup
from typing import List
def get_requirements()->List[str]:
    """"This function return list of requirement"""
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #readlines from the file
            lines = file.readlines()
            #process each line
            for line in lines:
                requirement=line.strip()
                ##ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project directory.")
    return requirement_lst


setup(
    name ="NetworkSecurity",
    version ="0.0.1",
    author="vinayak",
    author_email="Vinayakmbmb123@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)