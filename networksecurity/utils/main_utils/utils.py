import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import numpy as np
import sys
#import dill
import pickle



def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    :raises NetworkSecurityException: If the file cannot be read or parsed.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

#to write a report on drift we create write yaml file
def write_yaml_file(file_path: str, content: object,replace:bool=False) -> None:
    """
    Writes content to a YAML file.
    
    :param file_path: Path to the YAML file.
    :param content: Content to write to the file.
    :param replace: If True, replaces the existing file; if False, appends to it.
    :raises NetworkSecurityException: If the file cannot be written.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

