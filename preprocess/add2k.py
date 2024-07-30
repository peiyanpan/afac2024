from http import HTTPStatus
import dashscope
import pandas as pd
def trans(query):
    response = dashscope.Generation.call(
    model='qwen-turbo',
    prompt="请将下列query换个说法输出。\n如“我打算用10000000元买三羊马的股票，如果按照三羊马的最高价来计算，我能买多少股呢？”->\"请问你知道：如果以三羊马的最高股价为基准，我使用100万元可以购买到多少股三羊马的股票？\"；“方正的总资产和总负债相差多少”-> \"我想知道，方正的总资产和总负债有多少差距\"；“有没有那种份额类型标为R的基金，而且在过去一个月里它的最大回撤在同类型中的排名是3654？\n”->“，你知道，过去一个月里最大回撤在同类型中的排名是3654，而且份额类型标为R的基金有什么？”\n直接输出转换后的结果，无需附加任何额外说明或补全测试语句的空缺，不要回答语句的问题。\n只输出一句话！！测试语句是：\n"+ query,
    seed=23456,
    top_p=0.8,
    result_format='message',
    enable_search=False,
    max_tokens=1500,
    temperature=0.85,
    repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        # print(response.output.choices[0].message.content)
        return response.output.choices[0].message.content;
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
 
def add2k(train_excel, train_out_excel, length):
    # load data
    query_df = pd.read_excel(train_excel, usecols=["query"]) 
    api_df = pd.read_excel(train_excel, usecols=["label"])

    query_data = query_df.iloc[:, 0].tolist() 
    api_data = api_df.iloc[:, 0].tolist()

    # transform data 
    new_query = []
    new_apis = api_data[:length]

    for i in range(length):
        new_line = trans(query_data[i])
        new_query.append(new_line)

    query_data.extend(new_query)
    api_data.extend(new_apis)

    data = {'query': query_data, 'label': api_data}

    df = pd.DataFrame(data)  
    df.to_excel(train_out_excel, index=False, engine='openpyxl')  