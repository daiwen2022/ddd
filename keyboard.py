from aiogram import types

back_to_main_keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardMarkup(text='⬅️', callback_data='main_page'))
back_to_edit_links_keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardMarkup(text='⬅️', callback_data='change_links'))

main_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
		types.InlineKeyboardMarkup(text='📝 Change message', callback_data='change_message'),
		types.InlineKeyboardMarkup(text='🔗 Links', callback_data='change_links')
		)

def hello_keyboard(all_links):
	markup = types.InlineKeyboardMarkup(row_width=2)
	all_links = (types.InlineKeyboardMarkup(text=name, url=url) for num, name, url in all_links)
	markup.add(*(all_links))
	return markup

def links_keyboard(all_links):
	markup = types.InlineKeyboardMarkup(row_width=1)
	for num, name, url in all_links:
		markup.row(
			types.InlineKeyboardMarkup(text='➖', callback_data=f'delete_url;{num}'),
			types.InlineKeyboardMarkup(text=name, url=url)
			)
	markup.add(
		types.InlineKeyboardMarkup(text='➕ Add link', callback_data='add_link'),
		types.InlineKeyboardMarkup(text='⬅️', callback_data='main_page')
		)
	return markup

