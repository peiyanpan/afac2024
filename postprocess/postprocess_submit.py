#coding=utf8
import json
# 下面两个文件路径，第一个是推理生成的generated_predictions.jsonl文件路径，第二个是要提交的文件的路径
with open('../result/tmp39.jsonl','r') as m, open('../submit/tmp39.jsonl','w') as n:
    for line in m.readlines():
        line_json = json.loads(line)
        predict_label = line_json['predict']
        n.write(predict_label + '\n')