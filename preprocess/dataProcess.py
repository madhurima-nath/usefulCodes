import json
import os

from preprocess import create_json_dict
from extract.download import get_cloud_client, download_file

class DataProcess:
    def __init__(
            self,
            cloud_configuration: dict,
            local_preprocessing_configuration: dict,
    ) -> None:
        self.cloud_config = cloud_configuration
        self.local_preprocessing_config = local_preprocessing_configuration
        self.local_folder = local_preprocessing_configuration.get("data_path")

    def setup_local_folder(Self) -> None:
        if not os.path.exists(self.local_folder):
            os.makedirs(self.local_folder)

    def download_files(self) -> None:
        self.setup_local_folder()

        session = get_cloud_client(self.cloud_config.get("credentials_profile_name"))

        # download file
        download_file(
            session,
            self.cloud_config.get("storage_name"),
            self.cloud_config.get("filepath"),
            self.local_folder 
            + self.local_preprocessing_config.get("filepath"),
        )

    def file_preprocess(self) -> None:
        # load json data file
        with open(
            self.local_folder
            + self.local_preprocessing_config.get("filename"),
            "r",
        ) as f:
            data = json.load(f)

        processedDict = create_json_dict.create_dict(data)

        # save preprocessed json
        with open(
            self.local_folder
            + self.local_preprocessing_config.get("preprocessed_filename"),
            "w",
        ) as outfile:
            json.dump(processedDict, outfile, indent=4)

    def get_preprocessed_data(self) -> dict:
        with open(
            self.local_preprocessing_config.get("data_path"),
            + self.local_preprocessing_config.get("preprocessed_filename"),
            "r",
        ) as json_file:
            return json.load(json_file)