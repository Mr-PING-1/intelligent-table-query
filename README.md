 # 表格数据的智能查询系统
 
 数据库原理与应用课程 Project 2026 — 题目一
 
 作者：彭昊翎 | 学号：42411099
 
 ## 项目简介
 
 基于 SSTQA-zh 数据集，实现一个对半结构化 Excel 表格的智能查询系统。
 系统能够：
 
 1. **解析 Excel 表格**：自动识别表格结构（规整二维表 / 键值对表 / 混合结构）
 2. **拆分并存入 SQLite**：根据数据特点将表格拆分为子表，存入关系数据库
 3. **自然语言查询**：接收中文问题，按查询语义路由到 SQL 或 LLM 路径
 4. **自动评估**：与 SSTQA-zh 标准答案对比，统计正确率
 
 ## 数据集
 
 SSTQA-zh：[ST-Raptor / SSTQA-zh](https://github.com/OpenDataBox/ST-Raptor/tree/master/data/SSTQA-zh)
 包含 100 个半结构化 Excel 表格 + 764 条测试查询
 三种查询类型：Content Match（内容匹配）、Numeric Computation（数值计算）、Semantic-Aware（语义理解）
 
 ## 系统架构
 
 Excel 表格 → 表格分析 & 拆分 → SQLite 存储
 
 用户查询 → 路由判断 → [SQL 查询 | DeepSeek LLM] → 答案
 
 评估对比 → 正确率报告
 
 ## 运行环境
 
 Python 3.8+
 依赖：openpyxl, openai, tqdm
 
 ## 使用前准备
 
 1. **配置 API Key**：打开 `config.py`，将 `DEEPSEEK_API_KEY` 替换为你的 DeepSeek API Key
 2. **安装依赖**：`pip install -r requirements.txt`
 3. **确保数据集**：SSTQA-zh 已下载到 `F:\Users\db_project_data\ST-Raptor\data\SSTQA-zh\`
 
 ## 使用方法
 
 python run.py
 
 程序会自动执行：
 1. 读取并解析所有 100 个 Excel 表格
 2. 存入 SQLite 数据库
 3. 遍历 764 条测试查询，逐条回答
 4. 与标准答案对比，输出评估报告
 
 ## 模块说明
 
 src/table_analyzer.py - 表格分析与结构拆分
 src/hybrid_store.py - SQLite 存储层
 src/query_router.py - 查询路由（关键词分类）
 src/query_handler.py - SQL 查询 + DeepSeek LLM 查询
 src/evaluator.py - 评估与正确率统计
 src/main.py - 主流程集成
 config.py - DeepSeek API 配置
 data_link.py - 数据集路径配置
 run.py - 一键运行入口
