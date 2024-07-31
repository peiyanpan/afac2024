import pandas as pd
import difflib
import json
from tqdm import tqdm
from extract_keywords import extractKeywords


class CreateTrainData:
    def __init__(self, standard_name_path, train_path, dev_path, test_path, train_out_jsonl, dev_out_jsonl, test_out_jsonl, simple_name_out_jsonl) -> None:
        self.prompt='query是：QUERY   query中提到的产品标准名可能是：PRODUCT'
        self.instruction = '你现在是一个金融领域专家，你的职责是编排api，以高效且精准地处理用户的各类金融查询query。你需要确保API能够智能解析用户的query，可能需要使用适当的金融数据标准名作为api的参数，并将api组合返回结果，最后把整个编排的api和最终结果整合成清晰、结构化的JSON格式输出。'
        self.standard_name_path = standard_name_path
        self.train_path = train_path
        self.dev_path = dev_path
        self.test_path = test_path
        self.train_out_jsonl = train_out_jsonl
        self.dev_out_jsonl = dev_out_jsonl
        self.test_out_jsonl = test_out_jsonl
        self.simple_name_out_jsonl = simple_name_out_jsonl
        self.standard_name = self.load_standard_name()
        self.keywords = set()  # 用于存储所有提取的关键词
    
    def load_standard_name(self):
        data_stock = pd.read_excel(self.standard_name_path,sheet_name='股票标准名')
        data_fund = pd.read_excel(self.standard_name_path,sheet_name='基金标准名')
        standard_name = data_stock['标准股票名称'].to_list()+data_fund['标准基金名称'].to_list()
        return standard_name
    
    def run(self):
        df_train = pd.read_excel(self.train_path)
        df_dev = pd.read_excel(self.dev_path)
        df_test_b = pd.read_excel(self.test_path)

        self.df_2_json(df_train, self.train_out_jsonl)
        self.df_2_json(df_dev, self.dev_out_jsonl)
        self.df_2_json(df_test_b, self.test_out_jsonl)
        self.save_keywords(self.simple_name_out_jsonl)  # 保存关键词到文件

    def df_2_json(self, df, json_file):
        with open(json_file, 'w',encoding='utf-8') as m:
            for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                query = row['query']
                if "哪些" not in query:
                    # 提取关键词
                    keyword = extractKeywords(index, query)
                    self.keywords.add(keyword)  # 记录提取的关键词

                    # 防止出现多余的符号，一概删掉
                    keyword = keyword.replace('。', ' ').replace('，', ' ').replace('、', '').replace('；', '') \
                        .replace(' ', '').replace("None", '').replace('关键词', '').replace('：', '')

                    if keyword == "":  # 可能是提取关键词出了问题
                        products = difflib.get_close_matches(query, self.standard_name, n=50, cutoff=0.0001)
                        products_str = '、'.join(products)
                    else:
                        products = difflib.get_close_matches(keyword, self.standard_name, n=20, cutoff=0.0001)
                        products_str = '、'.join(products)

                    if products_str == "":
                        input_ = self.prompt.replace('QUERY', query).replace('\n query中提到的产品标准名可能是：PRODUCT', '')
                    else:
                        input_ = self.prompt.replace('QUERY', query).replace('PRODUCT', products_str)
                else:
                    input_ = query

                try:
                    output_ = row['label']
                except:
                    output_ = 'mock'

                single_data = {'instruction': self.instruction, 'input': input_, 'output': output_}
                # 每生成一个结果写入一次，防止出现中断
                m.write(json.dumps(single_data, ensure_ascii=False) + '\n')

    def save_keywords(self, json_file):
        with open(json_file, 'w',encoding='utf-8') as f:
            for keyword in self.keywords:
                f.write(json.dumps({"简称": keyword}, ensure_ascii=False) + '\n')
