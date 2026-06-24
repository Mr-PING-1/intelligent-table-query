# -*- coding: utf-8 -*-
"""DeepSeek API 配置"""

# DeepSeek API 配置
# 请将下面的 your-api-key-here 替换为你的真实 API Key
DEEPSEEK_API_KEY = "your-api-key-here"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 查询路由 —— 适合走 SQL 直接查询的关键词
SQL_KEYWORDS = [
    "多少", "什么", "列出", "有哪些", "是什么", "哪个",
    "最大", "最小", "平均", "总和", "合计", "个数", "多少条"
]

# 查询路由 —— 适合走 LLM 推理的关键词
LLM_KEYWORDS = [
    "比较", "分析", "趋势", "为什么", "差异", "说明",
    "总结", "区别", "关系", "原因", "影响", "变化"
]
