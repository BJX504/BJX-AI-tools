import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from utils import read_data, generate_data_info, generate_code, execute_code
from config import BIOSTAT_ANALYSES, BIOSTAT_PLOTS

# 设置页面配置
st.set_page_config(
    page_title="生物统计 AI 代码生成工具",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 深色模式
st.markdown("""
<style>
    body {
        color: #FFFFFF;
        background-color: #1E1E1E;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #3498db;
        border-radius: 5px;
    }
    .stTextArea>div>div>textarea {
        color: #FFFFFF;
        background-color: #2D2D2D;
    }
    .stFileUploader>label {
        color: #FFFFFF;
    }
    .stDataFrame {
        color: #FFFFFF;
        background-color: #2D2D2D;
    }
    .stCodeBlock {
        background-color: #2D2D2D;
    }
    .stSelectbox>div>div>select {
        color: #FFFFFF;
        background-color: #2D2D2D;
    }
    .stTabs {
        color: #FFFFFF;
    }
    .stTab {
        color: #FFFFFF;
        background-color: #2D2D2D;
    }
    .stTab[data-baseweb="tab"][aria-selected="true"] {
        background-color: #3498db;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("生物统计 AI 代码生成工具")

# 侧边栏
with st.sidebar:
    st.header("工具设置")
    
    # 数据上传
    st.subheader("数据上传")
    uploaded_file = st.file_uploader(
        "选择数据文件", 
        type=["csv", "xlsx", "txt"],
        help="支持CSV、XLSX和TXT格式的文件"
    )
    
    # 分析类型选择
    st.subheader("分析类型")
    analysis_type = st.selectbox(
        "选择分析类型",
        BIOSTAT_ANALYSES,
        index=0
    )
    
    # 图表类型选择
    if analysis_type == "数据可视化":
        plot_type = st.selectbox(
            "选择图表类型",
            BIOSTAT_PLOTS,
            index=0
        )
    else:
        plot_type = None

# 主内容区
if uploaded_file is not None:
    # 读取数据
    try:
        df = read_data(uploaded_file)
        
        # 数据预览
        st.subheader("数据预览")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"数据集形状: {df.shape}")
            st.write("字段名:", list(df.columns))
        with col2:
            st.write("数据类型:")
            st.dataframe(df.dtypes.to_frame(), use_container_width=True)
        
        st.write("前10行数据:")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.write("基本统计信息:")
        st.dataframe(df.describe(), use_container_width=True)
        
        # 分析需求输入
        st.subheader("分析需求")
        col1, col2 = st.columns([3, 1])
        with col1:
            user_request = st.text_area(
                "详细描述您的分析需求",
                height=150,
                placeholder="例如：分析不同组之间的差异，绘制相关性热图，进行生存分析等"
            )
        with col2:
            st.write("\n")
            if st.button("自动生成需求", use_container_width=True):
                if analysis_type == "数据可视化" and plot_type:
                    user_request = f"使用{plot_type}可视化数据"
                else:
                    user_request = f"进行{analysis_type}"
        
        # 代码生成和运行
        if user_request:
            st.subheader("AI 生成代码")
            
            # 生成数据信息
            data_info = generate_data_info(df)
            
            # 生成代码
            if st.button("生成代码", use_container_width=True):
                with st.spinner("正在生成代码..."):
                    try:
                        code = generate_code(data_info, user_request)
                        
                        # 显示代码
                        st.code(code, language="python")
                        
                        # 复制代码按钮
                        if st.button("复制代码", use_container_width=True):
                            st.write("代码已复制到剪贴板")
                        
                        # 运行代码
                        st.subheader("运行结果")
                        if st.button("运行代码", use_container_width=True):
                            with st.spinner("正在运行代码..."):
                                try:
                                    # 创建命名空间
                                    namespace = {}
                                    namespace["df"] = df
                                    namespace["st"] = st
                                    namespace["pd"] = pd
                                    namespace["np"] = np
                                    namespace["plt"] = plt
                                    namespace["sns"] = sns
                                    
                                    # 执行代码
                                    exec(code, namespace)
                                    
                                except Exception as e:
                                    st.error(f"代码执行错误: {e}")
                    except Exception as e:
                        st.error(f"代码生成失败: {e}")
        
        # 数据导出
        st.subheader("数据导出")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("导出为CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="下载CSV文件",
                    data=csv,
                    file_name="analyzed_data.csv",
                    mime="text/csv"
                )
        with col2:
            if st.button("导出为Excel"):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                output.seek(0)
                st.download_button(
                    label="下载Excel文件",
                    data=output,
                    file_name="analyzed_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        with col3:
            if st.button("导出为JSON"):
                json_str = df.to_json(orient='records', force_ascii=False)
                st.download_button(
                    label="下载JSON文件",
                    data=json_str,
                    file_name="analyzed_data.json",
                    mime="application/json"
                )
        
    except Exception as e:
        st.error(f"数据读取失败: {e}")
else:
    st.info("请上传数据文件开始分析")

# 页脚
st.markdown("---")
st.markdown("生物统计 AI 代码生成工具 | 基于 Streamlit 和 iFlow API")
