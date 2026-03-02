import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import io
from config import IFLOW_API_KEY, IFLOW_API_URL, MODEL, SYSTEM_PROMPT, CODE_PROMPT_TEMPLATE

# 读取数据文件
def read_data(file):
    """读取上传的数据文件"""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    elif file.name.endswith('.txt'):
        return pd.read_csv(file, sep='\t')
    else:
        raise ValueError("不支持的文件格式")

# 生成数据信息
def generate_data_info(df):
    """生成数据集信息"""
    data_info = f"""
    数据集形状: {df.shape}
    字段名: {list(df.columns)}
    数据类型:
    {df.dtypes}
    基本统计信息:
    {df.describe().to_string()}
    前5行数据:
    {df.head().to_string()}
    """
    return data_info

# 调用iFlow API生成代码
def generate_code(data_info, user_request):
    """调用iFlow API生成Python代码"""
    prompt = CODE_PROMPT_TEMPLATE.format(data_info=data_info, user_request=user_request)
    
    response = requests.post(
        IFLOW_API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IFLOW_API_KEY}"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API调用失败: {response.status_code}")

# 执行代码
def execute_code(code, df):
    """执行生成的代码"""
    namespace = {}
    namespace["df"] = df
    namespace["pd"] = pd
    namespace["np"] = np
    namespace["plt"] = plt
    namespace["sns"] = sns
    
    exec(code, namespace)
    return namespace

# 生成生物统计专用提示词
def generate_biostat_prompt(template, data_info, user_request):
    """生成生物统计专用提示词"""
    return template.format(data_info=data_info, user_request=user_request)
