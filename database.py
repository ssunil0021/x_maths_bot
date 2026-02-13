import asyncpg
import os
from datetime import date

# Railway automatic DATABASE_URL provide karta hai
DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            # Table creation logic
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS maths_content (
                        id SERIAL PRIMARY KEY,
                        post_date DATE UNIQUE NOT NULL,
                        concept_title TEXT,
                        question_file_id TEXT,
                        solution_file_id TEXT DEFAULT NULL
                    );
                ''')

    async def add_question(self, post_date, title, file_id):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO maths_content (post_date, concept_title, question_file_id)
                VALUES ($1, $2, $3)
                ON CONFLICT (post_date) DO UPDATE SET question_file_id = $3, concept_title = $2
            ''', post_date, title, file_id)

    async def add_solution(self, post_date, file_id):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                UPDATE maths_content SET solution_file_id = $1 WHERE post_date = $2
            ''', file_id, post_date)

    async def get_content_by_date(self, target_date):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('SELECT * FROM maths_content WHERE post_date = $1', target_date)