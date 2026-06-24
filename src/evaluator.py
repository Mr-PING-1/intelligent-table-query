# -*- coding: utf-8 -*-
"""评估模块"""
import json
from tqdm import tqdm


def normalize(s):
    if s is None:
        return ""
    s = str(s).strip()
    s = s.replace(" ", "").replace(",", "").replace("，", "")
    s = s.replace("％", "%").replace("≧", ">=").replace("≤", "<=")
    s = s.replace("≥", ">=").replace("≈", "=")
    return s


def exact_match(pred, label):
    return normalize(pred) == normalize(label)


def partial_match(pred, label):
    p, l = normalize(pred), normalize(label)
    if not p or not l:
        return False
    return l in p or p in l


def evaluate(test_path, query_func):
    queries = []
    with open(test_path, "r", encoding="utf-8") as f:
        for line in f:
            queries.append(json.loads(line))
    total = len(queries)
    exact_ok = 0
    partial_ok = 0
    by_type = {}
    by_diff = {}

    for q in tqdm(queries, desc="评估进度"):
        pred = query_func(q)
        label = q["label"]
        typ = q.get("type", "Unknown")
        diff = q.get("difficulty", "Unknown")
        em = exact_match(pred, label)
        pm = partial_match(pred, label)
        if em:
            exact_ok += 1
        if pm or em:
            partial_ok += 1

        for d, key in [(by_type, typ), (by_diff, diff)]:
            if key not in d:
                d[key] = {"total": 0, "exact": 0, "partial": 0}
            d[key]["total"] += 1
            if em:
                d[key]["exact"] += 1
            if pm or em:
                d[key]["partial"] += 1

    return {
        "total": total,
        "exact_match": exact_ok,
        "exact_accuracy": exact_ok / total if total else 0,
        "partial_match": partial_ok,
        "partial_accuracy": partial_ok / total if total else 0,
        "by_type": by_type,
        "by_difficulty": by_diff,
    }


def print_report(result):
    print("=" * 50)
    print("           表格智能查询系统 — 评估报告")
    print("=" * 50)
    print(f"\n测试总数: {result['total']}")
    print(f"精确匹配: {result['exact_match']} / {result['total']}  "
          f"({result['exact_accuracy']*100:.2f}%)")
    print(f"宽松匹配: {result['partial_match']} / {result['total']}  "
          f"({result['partial_accuracy']*100:.2f}%)")
    print("\n--- 按查询类型 ---")
    for typ, stats in sorted(result["by_type"].items()):
        print(f"  {typ:20s}  {stats['total']:4d} 条  "
              f"精确 {stats['exact']/stats['total']*100:5.2f}%  "
              f"宽松 {stats['partial']/stats['total']*100:5.2f}%")
    print("\n--- 按难度 ---")
    for diff in ["Simple", "Medium", "Hard"]:
        if diff in result["by_difficulty"]:
            s = result["by_difficulty"][diff]
            print(f"  {diff:8s}  {s['total']:4d} 条  "
                  f"精确 {s['exact']/s['total']*100:5.2f}%  "
                  f"宽松 {s['partial']/s['total']*100:5.2f}%")
    print("=" * 50)
