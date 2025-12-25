#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time           : 2025-12-20 16:54
@Author         : tao
@Python Version : 3.13.3
@Desc           : None
"""

"""
事务执行示例：
sqls = [
    ("INSERT INTO domains(domain) VALUES (?)", ("example.com",)),
    ("INSERT INTO pages(url, domain_id) VALUES (?, ?)",
     ("https://example.com", 1)),
]

db.execute_transaction(sqls)
"""

import sqlite3
from contextlib import contextmanager
from typing import Iterable, Tuple, Any

class SQLiteDB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回 dict 风格
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    def execute_transaction(
        self,
        statements: Iterable[Tuple[str, tuple]],
        *,
        immediate: bool = False
    ):
        """
        执行多条 SQL，作为一个事务
        :param statements: [(sql, params), ...]
        :param immediate: 是否使用 BEGIN IMMEDIATE
        """
        conn = self.connect()
        try:
            if immediate:
                conn.execute("BEGIN IMMEDIATE")
            else:
                conn.execute("BEGIN")

            for sql, params in statements:
                conn.execute(sql, params)

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    def execute(self, sql: str, params=()):
        with self.connect() as conn:
            cur = conn.execute(sql, params)
            return cur

    def executemany(self, sql: str, params_list: Iterable[Iterable[Any]]):
        with self.connect() as conn:
            conn.executemany(sql, params_list)

    def query_one(self, sql: str, params: Iterable[Any] = ()):
        with self.connect() as conn:
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None

    def query_all(self, sql: str, params: Iterable[Any] = ()):
        with self.connect() as conn:
            cur = conn.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]


