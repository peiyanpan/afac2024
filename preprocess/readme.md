## 内容介绍

main.py: 数据预处理的整个过程    
add2k.py: 添加数据的过程。利用dashscope的文本生成API，调用qwen-turbo模型,输入提示语，对输入的原始数据地query进行改写。  
pre_process.py: 使用了qwen-turbo模型，通过给它提示语的方式使它分析query并把query中包含的股票或者基金简称提取出来，再进行从所有标准名中检索相似的。    
generate_instructions.py: 合并训练数据和验证数据，提取测试数据，并将它们保存最终结果为json格式可以训练的数据，存放在../ptuning/data文件夹下  
get_fullname.py: 获取全称，并将全称文件保存在preprocess\tmp_data文件夹下  
generate_dict.py: 生成词典，并将词典保存在postprocess文件夹下  


## 运行方法

```python3
python main.py
```