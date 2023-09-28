import subprocess
import threading
from datetime import datetime
from service.tools.log_utils import capture_output
from service.settings import Settings

my_settings = Settings()


def offline_task(file_path, script_name, start_df):
    command = ["bash", file_path]
    # command = ["bash", my_settings.dev_script_dir + "/" + script_name]
    print("=====>>>>> 自定义脚本，离线任务开始执行:", command, start_df)
    log_file_path = my_settings.logs_path + "custom_" + script_name + "_" + start_df
    with open(log_file_path + ".log", 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()

    end_df = datetime.now().strftime(my_settings.datatime_sft)
    print("===== 自定义脚本，离线任务执行完成: ", command, end_df)

