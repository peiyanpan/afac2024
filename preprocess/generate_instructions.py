import json
def generate_instructions(train_jsonl, dev_jsonl, test_jsonl, train_out_json, test_out_json):
    train_instructions = []
    test_instructions = []

    with open(test_jsonl, "r", encoding="utf-8") as file:
        for line in file:
            instruction = json.loads(line)
            test_instructions.append(instruction)

    with open(train_jsonl, "r", encoding="utf-8") as file:
        for line in file:
            instruction = json.loads(line)
            train_instructions.append(instruction)

    with open(dev_jsonl, "r", encoding="utf-8") as file:
        for line in file:
            instruction = json.loads(line)
            train_instructions.append(instruction)

    # 生成可以训练的指令数据
    with open(train_out_json, 'w', encoding='utf-8') as file: 
        json.dump(train_instructions, file, ensure_ascii=False, indent=4)

    with open(test_out_json, 'w', encoding='utf-8') as file: 
        json.dump(test_instructions, file, ensure_ascii=False, indent=4)