import sqlite3
import os
import re
from datetime import datetime

class DictRow(dict):
    """A dictionary that can also be accessed by integer index or key."""
    def __init__(self, cursor, row):
        super().__init__()
        for idx, col in enumerate(cursor.description):
            self[col[0]] = row[idx]

class SQLiteCursor:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()
        self._results = []
        self._row_idx = 0
        self.rowcount = -1
        self.lastrowid = None

    def execute(self, query, args=None):
        # Convert MySQL %s placeholder to SQLite ?
        # Handle escaped %%
        tokens = query.split('%%')
        converted_tokens = [re.sub(r'%s', '?', t) for t in tokens]
        sql = '%'.join(converted_tokens)

        # Basic replacements for MySQL-specific functions if any
        # e.g., NOW() -> datetime('now')
        sql = re.sub(r'\bNOW\(\)', "datetime('now')", sql, flags=re.IGNORECASE)

        try:
            if args is not None:
                # Convert args from dict or list/tuple to match ?
                if isinstance(args, dict):
                    # If dict was passed to %s
                    res = self._cursor.execute(sql, list(args.values()))
                else:
                    res = self._cursor.execute(sql, list(args))
            else:
                res = self._cursor.execute(sql)

            self.lastrowid = self._cursor.lastrowid
            
            # If it's a SELECT statement
            trimmed_sql = sql.strip().upper()
            if trimmed_sql.startswith('SELECT') or trimmed_sql.startswith('SHOW') or trimmed_sql.startswith('PRAGMA'):
                col_names = [d[0] for d in self._cursor.description] if self._cursor.description else []
                raw_rows = self._cursor.fetchall()
                self._results = [dict(zip(col_names, r)) for r in raw_rows]
                self._row_idx = 0
                self.rowcount = len(self._results)
                return self.rowcount
            else:
                self._results = []
                self._row_idx = 0
                self.rowcount = self._cursor.rowcount if self._cursor.rowcount >= 0 else 1
                return self.rowcount
        except Exception as e:
            # Re-raise with clean context
            raise e

    def fetchone(self):
        if self._row_idx < len(self._results):
            row = self._results[self._row_idx]
            self._row_idx += 1
            return row
        return None

    def fetchall(self):
        if self._row_idx < len(self._results):
            rows = self._results[self._row_idx:]
            self._row_idx = len(self._results)
            return rows
        return []

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass


class SQLiteConnection:
    def __init__(self, db_path):
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def cursor(self):
        return SQLiteCursor(self._conn)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def _init_db(self):
        cur = self._conn.cursor()
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_type VARCHAR(25) NOT NULL,
            user_image LONGTEXT NOT NULL,
            user_login TINYINT DEFAULT 0,
            examcredits INTEGER DEFAULT 7
        );

        CREATE TABLE IF NOT EXISTS teachers (
            tid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            test_type VARCHAR(75) NOT NULL,
            start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end TIMESTAMP,
            duration INTEGER NOT NULL,
            show_ans INTEGER NOT NULL,
            password VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            topic VARCHAR(100) NOT NULL,
            neg_marks INTEGER NOT NULL,
            calc TINYINT NOT NULL,
            proctoring_type TINYINT DEFAULT 0,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS students (
            sid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            qid VARCHAR(25),
            ans LONGTEXT,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS questions (
            questions_uid INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id VARCHAR(100) NOT NULL,
            qid VARCHAR(25) NOT NULL,
            q LONGTEXT NOT NULL,
            a VARCHAR(100) NOT NULL,
            b VARCHAR(100) NOT NULL,
            c VARCHAR(100) NOT NULL,
            d VARCHAR(100) NOT NULL,
            ans VARCHAR(10) NOT NULL,
            marks INTEGER NOT NULL,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS studenttestinfo (
            stiid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            time_left TIME NOT NULL,
            completed TINYINT DEFAULT 0,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS longqa (
            longqa_qid INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id VARCHAR(100) NOT NULL,
            qid VARCHAR(25) NOT NULL,
            q LONGTEXT NOT NULL,
            marks INTEGER,
            uid INTEGER
        );

        CREATE TABLE IF NOT EXISTS longtest (
            longtest_qid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            qid INTEGER NOT NULL,
            ans LONGTEXT NOT NULL,
            marks INTEGER NOT NULL,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS practicalqa (
            pracqa_qid INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id VARCHAR(100) NOT NULL,
            qid VARCHAR(25) NOT NULL,
            q LONGTEXT NOT NULL,
            compiler TINYINT NOT NULL,
            marks INTEGER NOT NULL,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS practicaltest (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            qid VARCHAR(25) NOT NULL,
            code LONGTEXT,
            input LONGTEXT,
            executed VARCHAR(125),
            marks INTEGER NOT NULL,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS proctoring_log (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            name VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            voice_db INTEGER DEFAULT 0,
            img_log LONGTEXT NOT NULL,
            user_movements_updown TINYINT NOT NULL,
            user_movements_lr TINYINT NOT NULL,
            user_movements_eyes TINYINT NOT NULL,
            phone_detection TINYINT NOT NULL,
            person_status TINYINT NOT NULL,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uid INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS window_estimation_log (
            wid INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) NOT NULL,
            test_id VARCHAR(100) NOT NULL,
            name VARCHAR(100) NOT NULL,
            window_event TINYINT NOT NULL,
            transaction_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uid INTEGER NOT NULL
        );
        ''')
        self._conn.commit()

        # Seed default test users if empty
        cur.execute("SELECT count(*) as cnt FROM users")
        row = cur.fetchone()
        if row and row[0] == 0:
            import base64
            # 1x1 transparent png / dummy jpeg base64
            dummy_img = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
            # Insert demo professor and student
            cur.execute("""
            INSERT INTO users (name, email, password, user_type, user_image, user_login, examcredits)
            VALUES (?, ?, ?, ?, ?, 0, 100)
            """, ("Professor Admin", "teacher@exam.com", "password123", "teacher", dummy_img))
            cur.execute("""
            INSERT INTO users (name, email, password, user_type, user_image, user_login, examcredits)
            VALUES (?, ?, ?, ?, ?, 0, 100)
            """, ("Student Demo", "student@exam.com", "password123", "student", dummy_img))
            self._conn.commit()


class MySQL:
    def __init__(self, app=None):
        self.app = app
        self._connection = None
        self._use_sqlite = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    @property
    def connection(self):
        if self._connection is None:
            # First try PyMySQL to real MySQL if configured
            host = self.app.config.get('MYSQL_HOST', 'localhost')
            port = int(self.app.config.get('MYSQL_PORT', 3306))
            user = self.app.config.get('MYSQL_USER', 'root')
            password = self.app.config.get('MYSQL_PASSWORD', '')
            db = self.app.config.get('MYSQL_DB', 'quizapp')

            try:
                import pymysql
                import pymysql.cursors
                conn = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=db,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                    connect_timeout=2
                )
                print(f"[MySQL] Successfully connected to MySQL at {host}:{port}/{db}")
                self._connection = conn
            except Exception as ex:
                print(f"[Database] MySQL connection failed ({ex}). Falling back to fast local SQLite database (quizapp.db).")
                db_path = os.path.join(os.path.dirname(__file__), 'DB', 'quizapp.db')
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                self._connection = SQLiteConnection(db_path)
                self._use_sqlite = True

        return self._connection
