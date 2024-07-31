## 基本介绍

`./data`存放训练与测试数据  
`./deepspeed`存放deepspeed配置文件  
`./models`存放模型  
`./saves`存放模型训练和推理结果  
`./src`存放模型训练和推理代码  
## 训练

### 模型下载

```bash
cd models
git lfs install
git clone https://www.modelscope.cn/qwen/Qwen-14B.git
```

### 开始训练
根据需求可更改`--model_name_or_path`以设置模型路径
```bash
bash train.sh
```
训练后的模型保存在`./saves/train_output`


## 推理

### 下载我们训练好的模型（可选）

```bash
cd saves/models
git lfs install
git clone https://www.modelscope.cn/SugerFREE/service_lab_fine_tuned_qwen_14b.git
```
### 开始推理
根据需求可更改`--model_name_or_path`以设置模型路径
```bash
bash test.sh
```
推理结果保存在`./saves/eval_output`