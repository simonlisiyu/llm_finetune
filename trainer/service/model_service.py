# __author__ "lisiyu"
# date 2023/10/28
from ..settings import Settings

my_settings = Settings()


def get_template_list() -> list[str]:
    keys = my_settings.task_params.keys()
    to_remove = ['script', 'job_general', 'hparams_general', 'eval_general']
    template_list = [element for element in keys if element not in to_remove]
    return template_list
