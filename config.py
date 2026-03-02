import os

# iFlow API 配置
IFLOW_API_KEY = os.environ.get("IFLOW_API_KEY", "your_iFlow_api_key_here")
IFLOW_API_URL = "https://api.iflowai.com/v1/chat/completions"
# 模型配置
MODEL = "glm-5"

# 系统提示词
SYSTEM_PROMPT = "你是一个专业的生物统计和数据分析助手，擅长使用Python进行生物医学数据分析、统计建模和可视化。你熟悉各种生物统计方法，包括但不限于：描述性统计、假设检验、方差分析、回归分析、生存分析、聚类分析等。"

# 代码生成提示词模板
CODE_PROMPT_TEMPLATE = """
请根据以下数据集信息和用户需求，生成完整的可运行Python代码：

数据集信息：
{data_info}

用户需求：
{user_request}

要求：
1. 只输出可运行的Python代码，不要有任何解释或多余内容
2. 使用pandas处理数据
3. 使用seaborn和matplotlib进行可视化
4. 使用scipy和statsmodels进行统计分析
5. 代码应该直接读取已加载的数据（变量名：df）
6. 确保代码可以直接运行，不需要额外的依赖安装
7. 对于图表，使用streamlit的st.pyplot()函数显示
8. 对于统计结果，使用streamlit的st.write()函数显示
9. 对于生物统计分析，请使用专业的统计方法和参数
10. 确保代码具有良好的可读性和注释
"""

# 生物统计专用分析类型
BIOSTAT_ANALYSES = [
    "描述性统计分析",
    "相关性分析",
    "方差分析",
    "回归分析",
    "生存分析",
    "聚类分析",
    "假设检验",
    "数据可视化"
]

# 生物统计常用图表类型
BIOSTAT_PLOTS = [
    "相关性热图",
    "箱线图",
    "散点图",
    "直方图",
    "折线图",
    "饼图",
    "生存曲线",
    "ROC曲线"
]

