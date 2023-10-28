import os
import csv
import json
import pandas as pd
from ...settings import Settings
from ...model import DataSetInfo, ScriptInfo

my_settings = Settings()


# 记录执行日志到 CSV 文件
def write_csv_file(method_name, *args):
    log_entry = [method_name] + list(args)
    print("log_entry: ", log_entry)

    # 写入 CSV 文件
    with open(my_settings.log_dir + method_name + '_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)


def read_csv_file(method_name):
    data = []
    with open(my_settings.log_dir + method_name + '_log.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            data.append(row)
    return data


def read_dataset_info(file_path):
    datasets = []
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    for key in json_data.keys():
        json_obj = json_data.get(key)
        dataset = DataSetInfo(
            key,
            json_obj.get("upload_at"),
            json_obj.get("data_count"),
            "data/" + json_obj.get("file_name"))
        datasets.append(dataset)

    return datasets


def write_json_to_excel(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    dir_path = "/".join(file_path.split("/")[:-1])
    excel_name = file_path.split("/")[-1].split('.')[0] + "_out.xlsx"
    excel_path = dir_path + "/" + excel_name
    df.to_excel(excel_path, index=False)
    return excel_path, excel_name


def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"文件 {file_path} 已成功删除"
    except OSError as e:
        return f"删除文件 {file_path} 时出错: {e}"


def validate_json(json_data):
    try:
        json_arr = json.loads(json_data)
    except ValueError as err:
        return False, err
    return True, None, len(json_arr)


def append_to_json(file_path, data):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    json_data.update(data)
    with open(file_path, 'w') as file:
        json.dump(json_data, file, ensure_ascii=False)


def delete_key_in_json(file_path, key_name):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    if key_name in json_data:
        del json_data[key_name]
        with open(file_path, 'w') as file:
            json.dump(json_data, file, ensure_ascii=False)


def create_directory(filename, target_folder):
    # 获取目录名称
    directory_name = filename.split('.')[0]
    # 拼接目录路径
    directory_path = os.path.join(target_folder, directory_name)
    # 如果目录不存在，则创建目录
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path, directory_name


def get_files(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append({"filename": filename, "path": directory + "/" + filename})
    return files


def get_directories(directory):
    directories = []
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            directories.append({"filename": filename, "path": directory + "/" + filename})
    return directories


def get_directories_and_files(directory):
    dict_ = {}
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            files = get_files(directory + "/" + filename)
            dict_[filename] = files
    return dict_


def excel_to_json(excel_file):
    df = pd.read_excel(excel_file)
    json_list = []
    for _, row in df.iterrows():
        json_dict = {
            "instruction": str(row['instruction']),
            "input": str(row['input']) if not pd.isna(row['input']) else '',
            "output": str(row['output']) if not pd.isna(row['output']) else ''
        }
        json_list.append(json_dict)

    return json_list


def read_script_info():
    scripts = []
    with open(my_settings.dev_script_dir + '/script_info.json', 'r') as file:
        json_data = json.load(file)
    for key in json_data.keys():
        json_obj = json_data.get(key)
        dataset = ScriptInfo(
            key,
            json_obj.get("filepath"),
            json_obj.get("type"),
            json_obj.get("descript"),
            json_obj.get("upload_at"),
            json_obj.get("update_at")
            )
        scripts.append(dataset)

    return scripts

