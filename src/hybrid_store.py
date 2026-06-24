# -*- coding: utf-8 -*-
"""存储层 —— 将表格文本存入 SQLite"""
import sqlite3


class HybridStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA encoding = 'UTF-8'")
        self._init_meta()

    def _init_meta(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tables (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id   INTEGER,
                sheet_name TEXT,
                text_data  TEXT,
                col_count  INTEGER,
                row_count  INTEGER
            )
        """)
        self.conn.commit()

    def store(self, parsed):
        cur = self.conn.cursor()
        data = parsed["data"]
        text = parsed["text"]
        col_cnt = max((len(r) for r in data), default=0)
        row_cnt = len([r for r in data if any(c is not None for c in r)])
        cur.execute(
            "INSERT INTO tables (table_id, sheet_name, text_data, col_count, row_count) VALUES (?, ?, ?, ?, ?)",
            (parsed["table_id"], parsed["sheet_name"], text, col_cnt, row_cnt)
        )
        self.conn.commit()

    def get_table_count(self, table_id):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tables WHERE table_id = ?", (table_id,))
        return cur.fetchone()[0]

    def get_context(self, table_id):
        cur = self.conn.cursor()
        cur.execute("SELECT text_data FROM tables WHERE table_id = ?", (table_id,))
        rows = cur.fetchall()
        if not rows:
            return ""
        return "\n\n---\n\n".join(r[0] for r in rows)

    def search_text(self, table_id, keyword):
        """在表格文本中搜索关键词，返回匹配的行"""
        if not keyword or len(keyword) < 2:
            return []
        context = self.get_context(table_id)
        if not context:
            return []
        result = []
        for line in context.split("\n"):
            if keyword in line:
                result.append(line.strip())
        return result

    def close(self):
        self.conn.close()

    def clear(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tables")
        self.conn.commit()
