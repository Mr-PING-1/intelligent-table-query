# -*- coding: utf-8 -*-
"""一键运行脚本"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.main import run_evaluation
if __name__ == "__main__":
    run_evaluation()
