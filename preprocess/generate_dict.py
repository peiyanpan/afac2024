import jsonlines
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# 读取简称文件
def read_abbreviations(file_path):
    abbreviations = []
    with jsonlines.open(file_path) as reader:
        for index, line in enumerate(reader.iter(skip_invalid=True)):
            if line and '简称' in line and isinstance(line['简称'], str):
                abbreviations.append(line['简称'])
            else:
                print(f"Issue with abbreviation at line {index+1}: {line}")
    return abbreviations

# 读取全称文件
def read_fullnames(file_path):
    fullnames = []
    with jsonlines.open(file_path) as reader:
        for index, line in enumerate(reader.iter(skip_invalid=True)):
            if line and '全称' in line and isinstance(line['全称'], str):
                fullnames.append(line['全称'])
            else:
                print(f"Issue with full name at line {index+1}: {line}")
    return fullnames

# 匹配简称和全称
def match_abbreviations_to_fullnames(abbreviations, fullnames):
    matches = []
    for abbr in abbreviations:
        if abbr:
            best_match = process.extractOne(abbr, fullnames, scorer=fuzz.partial_ratio)
            matches.append({"简称": abbr, "全称": best_match[0] if best_match else None})
    return matches

# 保存匹配结果到jsonl文件
def save_matches_to_jsonl(matches, output_file):
    with jsonlines.open(output_file, 'w') as writer:
        for match in matches:
            writer.write(match)

