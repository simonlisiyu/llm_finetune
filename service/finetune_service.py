import subprocess
import threading
from datetime import datetime
from service.tools.log_utils import capture_output
from service.tools.file_utils import write_csv_file
from service.settings import Settings

my_settings = Settings()


def offline_finetune_task(model_path: str, train_data_path: str, hparams: dict, start_df: str):
    finetune_script = my_settings.script[model_path]['finetune']
    script_args = [model_path,
                   train_data_path,
                   hparams['epochs'],
                   my_settings.script['finetune_checkpoint'],
                   my_settings.script['max_node_num'],
                   my_settings.script['max_process_num'],
                   my_settings.script['master_ip'],
                   my_settings.script['master_port'],
                   hparams['gpus'],
                   hparams['lr'],
                   hparams['per_device_train_batch_size'],
                   hparams['gradient_accumulation_steps'],
                   hparams['lr_scheduler_type'],
                   my_settings.script[model_path]['quantization_bit'],
                   hparams['max_source_length'],
                   hparams['max_target_length'],
                   hparams['max_samples'],
                   ]
    command = [finetune_script] + script_args
    # start_df = datetime.now().strftime(datatime_sft)
    log_file_path = my_settings.logs_path + model_path + "_" + my_settings.finetune_log_prefix + "_" + start_df
    print("=====>>>>> 离线任务开始执行:", command, start_df)
    with open(log_file_path + ".log", 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()

    end_df = datetime.now().strftime(my_settings.datatime_sft)
    print("===== 离线任务执行完成: ", command, end_df)
    write_csv_file("offline_finetune_task", start_df, end_df, model_path, train_data_path, hparams,
                   log_file_path)


def copy_file_to_directory(valid_data_file):
    script_args = [valid_data_file, my_settings.base_data_dir, valid_data_file.split(".")[0]]
    command = [my_settings.file_copy_script] + script_args
    print("=====>>>>> 将文件拷贝到指定路径:", command)
    with open("copy_data_file" + ".log", 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()
    return valid_data_file.split(".")[0]