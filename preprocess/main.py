import dashscope
from add2k import add2k
from pre_process import CreateTrainData
from generate_instructions import generate_instructions

# settings
dashscope.api_key = "sk-8b43e7cbebe64ed2bbdb27dfd29cec7e"

train_excel = "../data-0520/train.xlsx"
dev_excel = '../data-0520/dev.xlsx'
test_excel = '../data-0520/test_b_without_label.xlsx'
standard_name_path = '../data-0520/标准名.xlsx'

train_out_excel = "../data-0520/train_add2000.xlsx"

train_jsonl= './tmp_data/train.jsonl'
dev_jsonl =  './tmp_data/dev.jsonl'
test_jsonl = './tmp_data/test.jsonl'

train_json = '../ptuning/data/train.json'
test_json =  '../ptuning/data/test.json'

# add data
print('start add data:')
add2k(train_excel, train_out_excel, 2000)
train_excel = train_out_excel

# create training data
print('start create training data:')
p = CreateTrainData(standard_name_path, train_excel, dev_excel, test_excel, train_jsonl, dev_jsonl, test_jsonl)
p.run()

# merge train and dev
print('start generate instructions:')
generate_instructions(train_jsonl, dev_jsonl, test_jsonl, train_json, test_json)