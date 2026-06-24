# -*- coding: utf-8 -*-
"""查询处理器 —— SQL 关键词搜索 & LLM 路径"""
from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


_client = None


def _get_client():
    global _client
    if _client is None:
        if DEEPSEEK_API_KEY == "your-api-key-here":
            raise ValueError("请先在 config.py 中填入 DeepSeek API Key")
        _client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    return _client


# ---- 关键词搜索（SQL 路径） ----
def _extract_keywords(query):
    """从查询中提取短关键词（2~6 字的中文片段）"""
    punct = set("，。、？：；""''「」【】《》（）—…· \t,.?!;:()[]{}")
    chars = [c for c in query if c not in punct and not c.isdigit()]
    result = set()
    for i in range(len(chars)):
        for j in range(i + 2, min(i + 5, len(chars) + 1)):
            word = "".join(chars[i:j])
            if len(word) >= 2:
                result.add(word)
    return sorted(result, key=len, reverse=True)[:20]


def sql_query(store, query, table_id):
    keywords = _extract_keywords(query)
    seen = set()
    results = []
    for kw in keywords:
        matches = store.search_text(table_id, kw)
        for line in matches:
            if line not in seen:
                seen.add(line)
                results.append(line)
        if len(results) >= 5:
            break
    return "；".join(results[:5]) if results else None


# ---- LLM 路径 ----
SYSTEM_PROMPT = """你是一个智能表格问答助手。用户会提供表格内容和一个中文问题。
请根据表格内容回答用户的问题，只输出答案本身，不要任何多余的解释。
如果表格中没有足够信息，回答"无法从表格中确定"。"""


def llm_query(store, query, table_id):
    client = _get_client()
    context = store.get_context(table_id)
    if not context:
        return "无法找到相关表格数据"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"表格数据:\n{context}\n\n问题: {query}"}
    ]
    try:
        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.1,
            max_tokens=512
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM 调用失败] {e}"
