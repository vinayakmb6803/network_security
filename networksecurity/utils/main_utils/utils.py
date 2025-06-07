import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import numpy as np
import sys
#import dill
import pickle
import sklearn
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score



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
    

def save_numpy_array_data(file_path:str, array:np.array):
    """
    Saves a NumPy array to a file using pickle.
    
    :param file_path: Path to the file where the array will be saved.
    :param array: NumPy array to save.
    :raises NetworkSecurityException: If the array cannot be saved.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def save_object(file_path:str,obj:object) -> None:
    try:
        logging.info("Entered the save_object method")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            #dill.dump(obj, file_obj)
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def load_object(file_path: str) -> object:
    """
    Loads an object from a file using pickle.
    
    :param file_path: Path to the file from which the object will be loaded.
    :return: The loaded object.
    :raises NetworkSecurityException: If the object cannot be loaded.
    """
    try:
        if not os.path.exists(file_path):
            raise Exception("The file {file_path} does not exist.")
        with open(file_path, 'rb') as file_obj:
            #return dill.load(file_obj)
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads a NumPy array from a file.
    
    :param file_path: Path to the file from which the array will be loaded.
    :return: The loaded NumPy array.
    :raises NetworkSecurityException: If the array cannot be loaded.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    


def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report={}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs =GridSearchCV(model, para, cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred =model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        logging.info(f"Model report: {report}")
        return report



    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

    


