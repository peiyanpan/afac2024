#coding=utf8
import json

# 明确指定文件编码格式为UTF-8
def submit():
    with open('../postprocess/temp.jsonl', 'r', encoding='utf-8') as m, open('../postprocess/submit.jsonl', 'w', encoding='utf-8') as n:
        for line in m.readlines():
            line_json = json.loads(line)
            predict_label = line_json['predict']
            n.write(predict_label + '\n')
