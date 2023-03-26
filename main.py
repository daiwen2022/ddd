import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram.types import ParseMode
from aiogram.utils import executor

from states import *
from keyboard import *
from data.config import *
from sqlite import get_all_links, add_link, delete_link, get_message_text, update_message_text

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def members_handler(message: types.Message):
	message_text, all_links = await asyncio.gather(get_message_text(), get_all_links())
	mess = await message.answer(message_text, reply_markup=hello_keyboard(all_links))
	await message.delete()

@dp.message_handler(content_types=[ContentType.LEFT_CHAT_MEMBER, ContentType.PINNED_MESSAGE, ContentType.NEW_CHAT_TITLE, ContentType.NEW_CHAT_PHOTO, ContentType.DELETE_CHAT_PHOTO, ContentType.GROUP_CHAT_CREATED])
async def members_handler(message: types.Message): 
	try:
		await message.delete()	
	except: pass
@dp.message_handler(commands='start', state='*')
async def message_handler(message: types.Message):
	user_id = message.from_user.id
	if not user_id in ADMIN_LIST:
		return
	await message.answer('<b>hello Admin!</b>', reply_markup=main_keyboard)

@dp.callback_query_handler(text='main_page', state='*') 
async def callback_main_page(call: types.CallbackQuery, state: FSMContext):
	user_id = call.from_user.id
	if not user_id in ADMIN_LIST:
		return
	await call.message.edit_text('<b>hello Admin!</b>', reply_markup=main_keyboard)
	await call.answer()

@dp.callback_query_handler(text='change_message', state='*') 
async def callback_change_message(call: types.CallbackQuery, state: FSMContext):
	if not call.from_user.id in ADMIN_LIST:
		return
	await call.message.edit_text('✍️ Enter new message text:', reply_markup=back_to_main_keyboard)
	await UpdateMessageText.get_message_text.set()
	await call.answer()

@dp.message_handler(state=UpdateMessageText.get_message_text)
async def message_change_message(message: types.Message, state: FSMContext):
	await state.finish()
	message_text = message.text
	await update_message_text(message_text)
	await message.answer('✅ Message text changed!', reply_markup=back_to_main_keyboard)

@dp.callback_query_handler(text='change_links', state='*') 
async def callback_change_links(call: types.CallbackQuery, state: FSMContext):
	if not call.from_user.id in ADMIN_LIST:
		return
	all_links = await get_all_links()
	await call.message.edit_text('All links:', reply_markup=links_keyboard(all_links))
	await call.answer()	

@dp.callback_query_handler(text_startswith='delete_url', state='*') 
async def callback_change_links(call: types.CallbackQuery, state: FSMContext):
	if not call.from_user.id in ADMIN_LIST:
		return
	num = call.data.split(';')[1]
	await delete_link(num)
	await call.answer('✅ Link deleted!')
	await callback_change_links(call, state)

@dp.callback_query_handler(text='add_link', state='*') 
async def callback_add_link(call: types.CallbackQuery, state: FSMContext):
	if not call.from_user.id in ADMIN_LIST:
		return
	await call.message.edit_text('✍️ Enter button name:', reply_markup=back_to_edit_links_keyboard)
	await AddLink.get_name.set()
	await call.answer()

@dp.message_handler(state=AddLink.get_name)
async def message_change_message(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await message.answer('✍️ Enter link:', reply_markup=back_to_edit_links_keyboard)
	await AddLink.get_link.set()

@dp.message_handler(state=AddLink.get_link)
async def message_change_message(message: types.Message, state: FSMContext):
	link = message.text
	if not '.' in link or not 'http' in link:
		await message.answer('❌ Wrond format!\n✍️ Enter link:', reply_markup=back_to_edit_links_keyboard)
		return
	async with state.proxy() as data:
		name = data['name']
	await state.finish()
	await add_link(name, link)
	await message.answer('✅ Link added', reply_markup=back_to_edit_links_keyboard)

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	executor.start_polling(dp, skip_updates=True)
