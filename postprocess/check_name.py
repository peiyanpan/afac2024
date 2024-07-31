import json
import pandas as pd
import re

# 读取标准名称的Excel文件
def read_standard_names_from_excel(file_path):
    data_stock = pd.read_excel(file_path, sheet_name='股票标准名')
    data_fund = pd.read_excel(file_path, sheet_name='基金标准名')
    standard_names = data_stock['标准股票名称'].to_list() + data_fund['标准基金名称'].to_list()
    return standard_names

# 读取词典文件
def read_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            dictionary[entry["简称"]] = entry["全称"]
    return dictionary

# 读取jsonl文件并处理
def process_jsonl_file(file_path, standard_names_set, dictionary):
    output = []
    query_counter = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        query_counter += 1  # 增加计数器
        try:
            data = json.loads(line.strip())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {line.strip()}")
            print(f"Error message: {e}")
            output.append(line.strip())
            continue

        prompt = data.get("prompt", "")
        query_match_1 = re.search(r'query是：(.*?)\s+query中提到的产品标准名可能是：', prompt)
        query_match_2 = re.search(r'query是：(.*?)\s', prompt)
        if query_match_1:
            query = query_match_1.group(1)
        else:
            query = query_match_2.group(1)
        
        if "query中提到的产品标准名可能是：" not in prompt:
            output.append(json.dumps(data, ensure_ascii=False))
            continue
        
        try:
            predict = json.loads(data.get("predict", "{}"))
        except json.JSONDecodeError as e:
            print(f"Error decoding 'predict' field on line: {line.strip()}")
            print(f"Error message: {e}")
            output.append(json.dumps(data, ensure_ascii=False))
            continue

        modified = False
        for api in predict.get("relevant APIs", []):
            required_parameters = api.get("required_parameters", [])
            if required_parameters and isinstance(required_parameters[0], list):
                first_param = required_parameters[0][0]
                if first_param not in standard_names_set:
                    # 检查词典中的“简称”
                    for abbr, full_name in dictionary.items():
                        if abbr in query:
                            api["required_parameters"][0][0] = full_name
                            modified = True
                            break

        if modified:
            data["predict"] = json.dumps(predict, ensure_ascii=False)

        output.append(json.dumps(data, ensure_ascii=False))

    return output

# 保存处理后的jsonl文件
def save_processed_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(item + '\n')

