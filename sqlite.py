import aiosqlite
import asyncio
from datetime import datetime, timedelta
from data.config import DB_PATH

async def create_table_links():
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		# await cursor.execute('DROP TABLE links')
		await cursor.execute('CREATE TABLE IF NOT EXISTS links(num INTEGER, name TEXT, url TEXT, PRIMARY KEY("num" AUTOINCREMENT))')

async def create_table_message_text():
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		# await cursor.execute('DROP TABLE message_text')
		await cursor.execute('CREATE TABLE IF NOT EXISTS message_text(num INTEGER, message_text TEXT, PRIMARY KEY("num" AUTOINCREMENT))')
		# await cursor.execute('INSERT INTO message_text(num) VALUES (1)')
		# await db.commit()
		
asyncio.run(create_table_links())
asyncio.run(create_table_message_text())


async def get_all_links():
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		await cursor.execute('SELECT num, name, url FROM links')
		return (await cursor.fetchall())

async def add_link(name, url):
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		await cursor.execute('INSERT INTO links(name, url) VALUES (?, ?)', (name, url))
		await db.commit()

async def delete_link(num):
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		await cursor.execute('DELETE FROM links WHERE num = ?', (num,))
		await db.commit()

async def get_message_text():
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		await cursor.execute('SELECT message_text FROM message_text')
		return (await cursor.fetchone())[0]

async def update_message_text(message_text):
	async with aiosqlite.connect(DB_PATH) as db:
		cursor = await db.cursor()
		await cursor.execute('UPDATE message_text SET message_text = ?', (message_text,))
		await db.commit()