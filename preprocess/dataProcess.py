import json
import os

from preprocess.create_json_dict import CreateGroupDict
from preprocess.desc_summarize import SummarizeDesc
from extract.download import get_cloud_client, download_file, upload_file



class DataProcess:
    def __init__(
            self,
            cloud_configuration: dict,
            local_filepath_config: dict,
    ) -> None:
        self.cloud_config = cloud_configuration
        self.local_filepath_config = local_filepath_config
        self.local_folder = local_filepath_config.get("data_path")


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
            + self.local_filepath_config.get("filepath"),
        )


    def upload_files(self) -> None:
        self.setup_local_folder()

        session = get_cloud_client(self.cloud_config.get("credentials_profile_name"))

        # upload file to cloud storage
        upload_file(
            session,
            self.cloud_config.get("storage_name"),
            self.cloud_config.get("download_filepath"),
            self.local_folder 
            + self.local_filepath_config.get("download_filepath"),
        )


    def file_preprocess(self) -> None:
        # load json data file
        with open(
            self.local_folder
            + self.local_filepath_config.get("json_data_filename"),
            "r",
        ) as f:
            data = json.load(f)

        processedDict = create_json_dict.create_dict(data)

        # save processed json
        with open(
            self.local_folder
            + self.local_filepath_config.get("processed_filename"),
            "w",
        ) as outfile:
            json.dump(processedDict, outfile, indent=4)


    def get_processed_data(self) -> dict:
        with open(
            self.local_filepath_config.get("data_path"),
            + self.local_filepath_config.get("processed_filename"),
            "r",
        ) as json_file:
            return json.load(json_file)
        
    
    def feature_summary(self, model) -> None:
        # save summarized features in a dict locally
        with open(
            self.local_folder
            + self.local_filepath_config.get("summarized_filename"),
            "r",
        ) as json_file:
            data = json.load(json_file)

        SummarizeDesc.feature_summary_dict(
            data,
            model,
            self.local_folder
            + self.local_filepath_config.get("summarized_filename"),
        )

    def get_feature_summary(self) -> dict:
        with open(
            self.local_filepath_config.get("data_path")
            + self.local_filepath_config.get("summarized_filename"),
            "r",
        ) as json_file:
            return json.load(json_file)