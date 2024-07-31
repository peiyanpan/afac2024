import dashscope
from add2k import add2k
from pre_process import CreateTrainData
from generate_instructions import generate_instructions
import generate_dict
import get_fullname

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
simple_name_jsonl = 'tmp_data/simple_name.jsonl'

train_json = '../ptuning/data/train.json'
test_json =  '../ptuning/data/test.json'


# add data
print('start add data:')
add2k(train_excel, train_out_excel, 2000)
train_excel = train_out_excel

# create training data
print('Start creating training data:')
p = CreateTrainData(
    standard_name_path=standard_name_path,
    train_path=train_excel,
    dev_path=dev_excel,
    test_path=test_excel,
    train_out_jsonl=train_jsonl,
    dev_out_jsonl=dev_jsonl,
    test_out_jsonl=test_jsonl,
    simple_name_out_jsonl=simple_name_jsonl
)
p.run()

# merge train and dev
print('start generate instructions:')
generate_instructions(train_jsonl, dev_jsonl, test_jsonl, train_json, test_json)

# create dictionary
print('start generate dictionary:')
input_file = '../ptuning/data/raw_train.json'
output_file = 'tmp_data/full_names.jsonl'
data = get_fullname.read_json_file(input_file)
full_names = get_fullname.extract_full_names(data)
get_fullname.save_to_jsonl(full_names, output_file)

abbr_file = 'tmp_data/simple_name.jsonl'
fullname_file = 'tmp_data/full_names.jsonl'
output_file = '../postprocess/dictionary.jsonl'
abbreviations = generate_dict.read_abbreviations(abbr_file)
fullnames = generate_dict.read_fullnames(fullname_file)
matches = generate_dict.match_abbreviations_to_fullnames(abbreviations, fullnames)
generate_dict.save_matches_to_jsonl(matches, output_file)