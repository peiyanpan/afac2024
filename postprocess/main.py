import json
import pandas as pd
import re
import check_name as check_name
import postprocess_submit as submit



# 处理文件并保存结果
input_file = '../ptuning/saves/eval/generated_predictions.jsonl'
output_file = '../postprocess/temp.jsonl'
standard_names_excel = '../data-0520/标准名.xlsx'
dictionary_file = 'dictionary.jsonl'

standard_names_set = check_name.read_standard_names_from_excel(standard_names_excel)
dictionary = check_name.read_dictionary(dictionary_file)
processed_data = check_name.process_jsonl_file(input_file, standard_names_set, dictionary)
check_name.save_processed_jsonl(processed_data, output_file)

submit.submit()