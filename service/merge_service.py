import subprocess
import threading
from datetime import datetime
from service.tools.log_utils import capture_output
from service.tools.file_utils import write_csv_file
from service.settings import Settings

my_settings = Settings()


def offline_merge_task(base_model, output_dir):
    merge_script = my_settings.script[base_model]['merge']
    script_args = [base_model, my_settings.script['finetune_checkpoint'], output_dir]
    command = [merge_script] + script_args
    start_df = datetime.now().strftime(my_settings.datatime_sft)
    log_file_path = my_settings.logs_path + output_dir + "_" + my_settings.finetune_log_prefix + "_" + start_df
    print("=====>>>>> 离线任务开始执行:", command)
    with open(log_file_path + ".log", 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()

    end_df = datetime.now().strftime(my_settings.datatime_sft)
    print("===== 离线任务执行完成: ", command, end_df)
    write_csv_file("offline_merge_task", start_df, end_df, base_model, output_dir, log_file_path)