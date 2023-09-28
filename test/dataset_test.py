import json
import pandas as pd


class DataSetInfo:
    def __init__(self, name, uptime, count, filepath):
        self.name = name
        self.uptime = uptime
        self.count = count
        self.filepath = filepath


def read_dataset_info(file_path):
    datasets = []
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    for key in json_data.keys():
        json_obj = json_data.get(key)
        dataset = DataSetInfo(key, json_obj.get("upload_at"), json_obj.get("data_count"), json_obj.get("file_name"))
        datasets.append(dataset)

    return datasets


def download_dataset_to_excel(file_path):
    # 加载 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    dir_path = "/".join(file_path.split("/")[:-1])
    excel_name = file_path.split("/")[-1].split('.')[0] + "_out.xlsx"
    print(dir_path)
    print(excel_name)
    df.to_excel('/Users/lisiyu/IdeaProjects/ALGO/llm_finetune/test/output.xlsx', index=False)


def excel_to_json(excel_file):
    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 将每行数据转换为字典，并添加到列表中
    json_list = []
    for _, row in df.iterrows():
        json_dict = {
            "instruction": str(row['instruction']),
            "input": str(row['input']) if not pd.isna(row['input']) else '',
            "output": str(row['output']) if not pd.isna(row['output']) else ''
        }
        json_list.append(json_dict)

    return json_list

# dsi1 = read_dataset_info("/Users/lisiyu/IdeaProjects/ALGO/llm_finetune/data/dataset_info.json")
# print(dsi1[0].name)  # 输出：test dataset
# print(dsi1[0].uptime)  # 输出：1800
# print(dsi1[0].count)  # 输出：10000
# print(dsi1[0].filepath)  # 输出：/path/to/my/dataset


# download_dataset_to_excel("/Users/lisiyu/IdeaProjects/ALGO/llm_finetune/data/self_cognition/self_cognition.json")

print(excel_to_json("/Users/lisiyu/Downloads/123_test.xlsx"))

# my_tuple = (0, 1)
# print(my_tuple[0])