from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
from typing import List, Dict
import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Expected number of columns: {number_of_columns}")
            logging.info(f"Number of columns in dataframe: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numerical_columns(self, train_df: pd.DataFrame, test_df: pd.DataFrame, check_columns: List[str]) -> bool:
        try:
            for col in check_columns:
                if col not in train_df.columns or col not in test_df.columns:
                    logging.warning(f"Numerical column {col} missing in either train or test dataset.")
                    return False
                if not pd.api.types.is_numeric_dtype(train_df[col]) or not pd.api.types.is_numeric_dtype(test_df[col]):
                    logging.warning(f"Column {col} is not numeric in either train or test dataset.")
                    return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report[column] = {
                    "p_value": float(is_same_dist.pvalue),
                    "is_found": is_found
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            error_message = ""

            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message += "Train dataframe does not have the required number of columns.\n"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message += "Test dataframe does not have the required number of columns.\n"

            status = self.validate_numerical_columns(train_dataframe, test_dataframe,
                                                     check_columns=self._schema_config['numerical_columns'])
            if not status:
                error_message += "Numerical columns validation failed.\n"

            if error_message:
                raise Exception(error_message)

            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)






