# -*- coding: utf-8 -*-
"""主流程：建库 → 查询 → 评估"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_link import DB_PATH, TEST_FILE, check_data_dir
from src.table_analyzer import analyze_table
from src.hybrid_store import HybridStore
from src.query_handler import sql_query, llm_query
from src.evaluator import evaluate, print_report


def build_database():
    if not check_data_dir():
        return False
    store = HybridStore(DB_PATH)
    store.clear()
    total_tables = 0
    for tid in range(1, 101):
        try:
            sections = analyze_table(tid)
            if sections:
                total_tables += 1
                for sec in sections:
                    store.store(sec)
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"  [跳过] 表格 {tid}: {e}")
    store.close()
    print(f"\n建库完成！处理了 {total_tables} 个表格。")
    return True


def query_single(test_entry, store):
    query = test_entry["query"]
    table_id = test_entry["table_id"]
    # 先尝试关键词搜索
    result = sql_query(store, query, table_id)
    if result:
        return result
    # 搜不到就走 LLM
    return llm_query(store, query, table_id)


def run_evaluation():
    print("=" * 50)
    print("   表格智能查询系统 — 端到端评估")
    print("=" * 50)
    print("\n[步骤 1] 建库中...")
    if not build_database():
        return
    print("\n[步骤 2] 评估中...")
    store = HybridStore(DB_PATH)
    def query_fn(entry):
        return query_single(entry, store)
    result = evaluate(TEST_FILE, query_fn)
    print_report(result)
    store.close()
    return result


if __name__ == "__main__":
    run_evaluation()
