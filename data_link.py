# -*- coding: utf-8 -*-
"""数据集路径配置"""
import os

# SSTQA-zh 数据集路径
DATA_DIR = r"F:\Users\db_project_data\ST-Raptor\data\SSTQA-zh"
TABLE_DIR = os.path.join(DATA_DIR, "table")
TEST_FILE = os.path.join(DATA_DIR, "test.jsonl")

# SQLite 数据库文件（存放在项目目录下）
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, "table_data.db")

def get_table_path(table_id):
    """根据表格 ID 获取 Excel 文件路径"""
    return os.path.join(TABLE_DIR, f"{table_id}.xlsx")

def check_data_dir():
    """检查数据集是否存在"""
    if not os.path.exists(TABLE_DIR):
        print(f"[WARNING] 数据集目录不存在: {TABLE_DIR}")
        return False
    return True
