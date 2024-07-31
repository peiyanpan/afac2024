import json
import jsonlines
import re

# 读取json文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 处理json数据
def extract_full_names(data):
    full_names = []
    for item in data:
        input_text = item.get("input", "")
        if "query中提到的产品标准名可能是：" in input_text:
            # 提取output中的全称名
            output_text = item.get("output", "")
            output_data = json.loads(output_text)
            relevant_apis = output_data.get("relevant APIs", [])
            for api in relevant_apis:
                required_parameters = api.get("required_parameters", [])
                if required_parameters and isinstance(required_parameters[0], list):
                    full_name = required_parameters[0][0]
                    full_names.append({"全称": full_name})
    return full_names

# 保存结果到jsonl文件
def save_to_jsonl(data, output_file):
    with jsonlines.open(output_file, 'w') as writer:
        for item in data:
            writer.write(item)

