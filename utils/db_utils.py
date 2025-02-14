import aiosqlite
from config import DB_NAME

#DB_NAME = 'quiz_bot.db'

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                score INTEGER
            )
        ''')

        await db.commit()

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def save_quiz_result(result):
    async with aiosqlite.connect(DB_NAME) as db:
        # Get current score or 0 if not exists
        async with db.execute('SELECT score FROM quiz_results WHERE user_id = ?', (result['user_id'],)) as cursor:
            current = await cursor.fetchone()
            current_score = current[0] if current else 0
        
        # If answer is correct, increment score
        new_score = current_score + (1 if result['correct'] else 0)
        
        await db.execute('''
            INSERT OR REPLACE INTO quiz_results (user_id, score) VALUES (?, ?)
        ''', (result['user_id'], new_score))
        await db.commit()

async def reset_user_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Reset question index to 0
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, 0)', (user_id,))
        # Reset score to 0
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, score) VALUES (?, 0)', (user_id,))
        await db.commit()

async def get_all_results():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id, score FROM quiz_results') as cursor:
            return await cursor.fetchall()

