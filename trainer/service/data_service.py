from .tools.file_utils import read_dataset_info
from ..settings import Settings

my_settings = Settings()


def get_dataset_info() -> dict:
    try:
        dataset_info = read_dataset_info(my_settings.base_dir + my_settings.data_file)
    except Exception as e:
        dataset_info = []
    return dataset_info