from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation,DataValidationConfig
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig
import os

import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion =DataIngestion(dataingestionconfig)
        logging.info("Starting the Data Ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion process completed successfully")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Starting the Data Validation process")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validatin process completed successfully")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("Starting the Data Transformation process")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Data Transformation process completed successfully")
        data_transformation_artifcat = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation artifact created successfully")
        print(data_transformation_artifcat)
    


        
    except Exception as e:
        raise NetworkSecurityException(e, sys)