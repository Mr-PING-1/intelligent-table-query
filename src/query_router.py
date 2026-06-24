# -*- coding: utf-8 -*-
"""查询路由模块"""
import re
from config import SQL_KEYWORDS, LLM_KEYWORDS


def classify_query(query):
    for kw in LLM_KEYWORDS:
        if kw in query:
            return "llm"
    for kw in SQL_KEYWORDS:
        if kw in query:
            return "sql"
    return "sql_first"


def extract_search_terms(query):
    stop_words = {"的", "是", "了", "在", "和", "与", "或",
                  "有", "不", "要", "把", "被", "让", "给",
                  "为", "就", "对", "等", "及", "所", "从",
                  "到", "以", "于", "上", "下", "中", "里",
                  "多少", "什么", "哪个", "哪些", "如何",
                  "列出", "找出", "查找", "搜索", "查询"}
    tokens = re.split(r'[\u3000-\u303f\uff00-\uffef，。、？：；""''「」【】\s,\?\.:;!\(\)\[\]]+', query)
    terms = set()
    for tok in tokens:
        tok = tok.strip()
        if len(tok) >= 2 and tok not in stop_words:
            terms.add(tok)
    return sorted(terms, key=len, reverse=True)


def match_table(terms, meta_rows):
    if not terms or not meta_rows:
        return []
    scored = []
    for row in meta_rows:
        _, sql_name, sub_name, sheet_name, typ, col_info, row_cnt = row
        score = 0
        for t in terms:
            if t in sub_name:
                score += 3
            if t in sheet_name:
                score += 1
            if t in col_info:
                score += 2
        if score > 0:
            scored.append((score, sql_name, sub_name, typ, col_info))
    scored.sort(key=lambda x: -x[0])
    return scored


def need_numeric(query):
    num_kw = ["最大", "最小", "平均", "总和", "合计", "总数", "多少条"]
    return any(kw in query for kw in num_kw)
