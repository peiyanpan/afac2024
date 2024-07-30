# -*- coding: utf-8 -*-
from http import HTTPStatus
import dashscope
def extractKeywords(id, query):
    
    response = dashscope.Generation.call(
        model='qwen-turbo',
        seed=1234,
        top_p=0.8,
        prompt="你现在是一个金融关键词提取机器人，我需要你从一个query中提取一个关于股票名或基金名的关键词，如果有关键词的话，你只需要给我关键词即可，不需要输出其他内容，加入没有股票或者基金名的关键词，回复我None就好。例如，query：嘉实鑫泰A成立多少年了，管理的资金规模是多少，风险等级如何？关键词：嘉实鑫泰A。例如：query：我想知道茂莱光学上周收盘价与上月最低价的差值是多少，并且这个差值相对于上周收盘价占的百分比是多少？ 关键词：茂莱光学。例如：query：我现在如果卖出我1年前用500块买的南方全天候A，和我昨天卖出的收益相比少了多少  关键词：南方全天候A。query:" + query + "关键词：",
        result_format='message',
        enable_search=False,
        max_tokens=1024,
        temperature=0.85,
        repetition_penalty=1.0
    )
    
    if response.status_code == HTTPStatus.OK:
        keyword = response.output.choices[0].message["content"]
        
    else:
        keyword = "None"
        with open("./log.txt", "a") as f:
            f.write(f"{id} {query} {response.message}\n")

    return keyword