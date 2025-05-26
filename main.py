from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation,DataValidationConfig
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
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
        logging.info("Data Validation process completed successfully")
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)