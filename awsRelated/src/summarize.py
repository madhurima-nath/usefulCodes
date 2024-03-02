from preprocess.preprocess import DataProcess
from main import ConfigParser, get_bedrock_llm

parser = ConfigParser()
config = parser.load_parameters()

aws_config = config.get("aws_configuration")
local_filepath_config = config.get("local_filepath_configuration")

llm = get_bedrock_llm(**aws_config)

data_process = DataProcess(aws_config, local_filepath_config)

# time taking process
# this step creates summarized file and stores it in local folder
data_process.feature_summary(llm)

# upload file to s3
data_process.upload_files()