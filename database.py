import sqlite3

def init_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            source TEXT,
            link TEXT UNIQUE,
            date_posted TEXT,
            fetched_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_jobs(jobs):
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    for job in jobs:
        try:
            cursor.execute('''
                INSERT INTO jobs (title, company, source, link, date_posted, fetched_on)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            ''', (job['title'], job['company'], job['source'], job['link'], job['date_posted']))
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, company, source, link, date_posted FROM jobs ORDER BY fetched_on DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows
