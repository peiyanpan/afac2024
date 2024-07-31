## 基本介绍

`./data`存放训练与测试数据  
`./deepspeed`存放deepspeed配置文件  
`./models`存放模型  
`./saves`存放模型训练和推理结果  
`./src`存放模型训练和推理代码  


## 模型下载

```bash
cd model
git lfs install
git clone https://www.modelscope.cn/qwen/Qwen-14B.git
```

## 训练

```bash
bash train.sh
```
训练后的模型保存在`./saves/Qwen1.5-14B/full/train_output`


## 推理

```bash
bash test.sh
```
推理结果保存在`./saves/Qwen1.5-14B/full/eval_output`